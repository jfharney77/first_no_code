import calendar as cal
from datetime import date

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TeamMemberForm, ChoreForm, RecurringChoreForm
from .models import TeamMember, Chore, RecurringChore
from .services import generate_chore_instances


# ── Calendar ─────────────────────────────────────────────────────────

def calendar_view(request, year=None, month=None):
    today = date.today()
    year = year or today.year
    month = month or today.month

    # Clamp to valid range
    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    c = cal.Calendar(firstweekday=6)  # Sunday first
    month_days = c.monthdatescalendar(year, month)

    # Date range for query
    first_day = month_days[0][0]
    last_day = month_days[-1][-1]

    chores = Chore.objects.filter(
        date__gte=first_day, date__lte=last_day
    ).select_related('assigned_to')

    chore_map = {}
    for chore in chores:
        chore_map.setdefault(chore.date, []).append(chore)

    # Build weeks with day data dicts
    weeks = []
    for week in month_days:
        week_data = []
        for d in week:
            week_data.append({
                'date': d,
                'chores': chore_map.get(d, []),
                'is_current_month': d.month == month,
                'is_today': d == today,
            })
        weeks.append(week_data)

    # Navigation
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month, prev_year = 12, year - 1

    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month, next_year = 1, year + 1

    context = {
        'weeks': weeks,
        'year': year,
        'month': month,
        'month_name': cal.month_name[month],
        'day_names': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today,
    }
    return render(request, 'chores/calendar.html', context)


# ── Chore CRUD ───────────────────────────────────────────────────────

def chore_create(request, date=None):
    initial = {}
    if date:
        initial['date'] = date
    if request.method == 'POST':
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chore created.')
            return redirect('chores:calendar')
    else:
        form = ChoreForm(initial=initial)
    return render(request, 'chores/chore_form.html', {'form': form})


def chore_detail(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    return render(request, 'chores/chore_detail.html', {'chore': chore})


def chore_update(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == 'POST':
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chore updated.')
            return redirect('chores:chore_detail', pk=pk)
    else:
        form = ChoreForm(instance=chore)
    return render(request, 'chores/chore_form.html', {'form': form, 'chore': chore})


def chore_delete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == 'POST':
        chore.delete()
        messages.success(request, 'Chore deleted.')
        return redirect('chores:calendar')
    return render(request, 'chores/chore_confirm_delete.html', {'chore': chore})


def chore_toggle_complete(request, pk):
    chore = get_object_or_404(Chore, pk=pk)
    chore.is_completed = not chore.is_completed
    chore.save(update_fields=['is_completed'])
    return redirect(request.META.get('HTTP_REFERER', 'chores:calendar'))


# ── Recurring Chores ─────────────────────────────────────────────────

def recurring_list(request):
    recurring = RecurringChore.objects.select_related('assigned_to').all()
    return render(request, 'chores/recurring_list.html', {'recurring': recurring})


def recurring_create(request):
    if request.method == 'POST':
        form = RecurringChoreForm(request.POST)
        if form.is_valid():
            rc = form.save()
            count = generate_chore_instances(rc)
            messages.success(request, f'Recurring chore created. {count} instances generated.')
            return redirect('chores:recurring_list')
    else:
        form = RecurringChoreForm()
    return render(request, 'chores/recurring_form.html', {'form': form})


def recurring_update(request, pk):
    rc = get_object_or_404(RecurringChore, pk=pk)
    if request.method == 'POST':
        form = RecurringChoreForm(request.POST, instance=rc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recurring chore updated.')
            return redirect('chores:recurring_list')
    else:
        form = RecurringChoreForm(instance=rc)
    return render(request, 'chores/recurring_form.html', {'form': form, 'recurring': rc})


def recurring_delete(request, pk):
    rc = get_object_or_404(RecurringChore, pk=pk)
    if request.method == 'POST':
        rc.delete()
        messages.success(request, 'Recurring chore deleted. Existing instances were kept.')
        return redirect('chores:recurring_list')
    return render(request, 'chores/recurring_confirm_delete.html', {'recurring': rc})


def recurring_generate(request, pk):
    rc = get_object_or_404(RecurringChore, pk=pk)
    count = generate_chore_instances(rc)
    messages.success(request, f'{count} new chore instances generated.')
    return redirect('chores:recurring_list')


# ── Team Members ─────────────────────────────────────────────────────

def team_member_list(request):
    members = TeamMember.objects.all()
    return render(request, 'chores/team_list.html', {'members': members})


def team_member_create(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added.')
            return redirect('chores:team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'chores/team_form.html', {'form': form})


def team_member_update(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated.')
            return redirect('chores:team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'chores/team_form.html', {'form': form, 'member': member})


def team_member_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted.')
        return redirect('chores:team_list')
    return render(request, 'chores/team_confirm_delete.html', {'member': member})

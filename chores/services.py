from datetime import date, timedelta
from .models import Chore, RecurringChore


def generate_chore_instances(recurring_chore, months_ahead=6):
    """Generate biweekly Chore instances for a RecurringChore.

    Creates instances every 14 days from start_date up to months_ahead months
    from today (or end_date, whichever is sooner). Skips dates that already
    have an instance linked to this recurring chore.

    Uses bulk_create to avoid triggering signals (no email spam).
    Returns the number of new instances created.
    """
    if not recurring_chore.is_active:
        return 0

    today = date.today()
    horizon = date(
        today.year + (today.month + months_ahead - 1) // 12,
        (today.month + months_ahead - 1) % 12 + 1,
        1,
    )

    end = recurring_chore.end_date or horizon
    end = min(end, horizon)

    # Get existing instance dates to avoid duplicates
    existing_dates = set(
        Chore.objects.filter(recurring_source=recurring_chore)
        .values_list('date', flat=True)
    )

    new_chores = []
    current = recurring_chore.start_date
    while current <= end:
        if current not in existing_dates:
            new_chores.append(Chore(
                title=recurring_chore.title,
                description=recurring_chore.description,
                date=current,
                assigned_to=recurring_chore.assigned_to,
                recurring_source=recurring_chore,
            ))
        current += timedelta(days=14)  # biweekly

    if new_chores:
        Chore.objects.bulk_create(new_chores)

    return len(new_chores)

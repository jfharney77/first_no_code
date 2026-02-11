from datetime import date, timedelta

from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

from .models import TeamMember, Chore, RecurringChore
from .services import generate_chore_instances


class TeamMemberTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = TeamMember.objects.create(name='Alice', email='alice@example.com')

    def test_list_view(self):
        resp = self.client.get(reverse('chores:team_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Alice')

    def test_create_member(self):
        resp = self.client.post(reverse('chores:team_create'), {
            'name': 'Bob',
            'email': 'bob@example.com',
        })
        self.assertRedirects(resp, reverse('chores:team_list'))
        self.assertTrue(TeamMember.objects.filter(name='Bob').exists())

    def test_update_member(self):
        resp = self.client.post(reverse('chores:team_update', args=[self.member.pk]), {
            'name': 'Alice Updated',
            'email': 'alice@example.com',
        })
        self.assertRedirects(resp, reverse('chores:team_list'))
        self.member.refresh_from_db()
        self.assertEqual(self.member.name, 'Alice Updated')

    def test_delete_member(self):
        resp = self.client.post(reverse('chores:team_delete', args=[self.member.pk]))
        self.assertRedirects(resp, reverse('chores:team_list'))
        self.assertFalse(TeamMember.objects.filter(pk=self.member.pk).exists())


class ChoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = TeamMember.objects.create(name='Alice', email='alice@example.com')
        self.chore = Chore.objects.create(
            title='Clean kitchen',
            date=date.today(),
            assigned_to=self.member,
        )

    def test_detail_view(self):
        resp = self.client.get(reverse('chores:chore_detail', args=[self.chore.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Clean kitchen')

    def test_create_chore(self):
        resp = self.client.post(reverse('chores:chore_create'), {
            'title': 'Mop floor',
            'date': date.today().isoformat(),
            'description': '',
            'assigned_to': '',
        })
        self.assertRedirects(resp, reverse('chores:calendar'))
        self.assertTrue(Chore.objects.filter(title='Mop floor').exists())

    def test_create_chore_with_date_prefill(self):
        target = date.today() + timedelta(days=3)
        resp = self.client.get(reverse('chores:chore_create_date', args=[target.isoformat()]))
        self.assertEqual(resp.status_code, 200)

    def test_update_chore(self):
        resp = self.client.post(reverse('chores:chore_update', args=[self.chore.pk]), {
            'title': 'Clean kitchen v2',
            'date': date.today().isoformat(),
            'description': '',
            'assigned_to': '',
        })
        self.assertRedirects(resp, reverse('chores:chore_detail', args=[self.chore.pk]))
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.title, 'Clean kitchen v2')

    def test_delete_chore(self):
        resp = self.client.post(reverse('chores:chore_delete', args=[self.chore.pk]))
        self.assertRedirects(resp, reverse('chores:calendar'))
        self.assertFalse(Chore.objects.filter(pk=self.chore.pk).exists())

    def test_toggle_complete(self):
        self.assertFalse(self.chore.is_completed)
        self.client.get(reverse('chores:chore_toggle', args=[self.chore.pk]))
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.is_completed)


class CalendarTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_calendar_home(self):
        resp = self.client.get(reverse('chores:calendar'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, date.today().year)

    def test_calendar_specific_month(self):
        resp = self.client.get(reverse('chores:calendar_month', args=[2026, 3]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'March')

    def test_calendar_shows_chores(self):
        Chore.objects.create(title='Test chore', date=date.today())
        resp = self.client.get(reverse('chores:calendar'))
        self.assertContains(resp, 'Test chore')


class RecurringChoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = TeamMember.objects.create(name='Alice', email='alice@example.com')

    def test_generate_instances(self):
        rc = RecurringChore.objects.create(
            title='Biweekly clean',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=56),
            assigned_to=self.member,
        )
        count = generate_chore_instances(rc)
        self.assertGreater(count, 0)
        # 56 days / 14 = 4 intervals, so 5 instances (day 0, 14, 28, 42, 56)
        self.assertEqual(count, 5)
        self.assertEqual(Chore.objects.filter(recurring_source=rc).count(), 5)

    def test_no_duplicates(self):
        rc = RecurringChore.objects.create(
            title='Biweekly clean',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=28),
        )
        count1 = generate_chore_instances(rc)
        count2 = generate_chore_instances(rc)
        self.assertGreater(count1, 0)
        self.assertEqual(count2, 0)  # no duplicates

    def test_inactive_generates_nothing(self):
        rc = RecurringChore.objects.create(
            title='Inactive',
            start_date=date.today(),
            is_active=False,
        )
        count = generate_chore_instances(rc)
        self.assertEqual(count, 0)

    def test_recurring_list_view(self):
        RecurringChore.objects.create(title='Weekly', start_date=date.today())
        resp = self.client.get(reverse('chores:recurring_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Weekly')

    def test_create_recurring_generates_instances(self):
        resp = self.client.post(reverse('chores:recurring_create'), {
            'title': 'New recurring',
            'description': '',
            'assigned_to': '',
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=28)).isoformat(),
            'is_active': 'on',
        })
        self.assertRedirects(resp, reverse('chores:recurring_list'))
        rc = RecurringChore.objects.get(title='New recurring')
        self.assertGreater(Chore.objects.filter(recurring_source=rc).count(), 0)

    def test_delete_recurring_keeps_instances(self):
        rc = RecurringChore.objects.create(
            title='To delete',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=28),
        )
        generate_chore_instances(rc)
        instance_count = Chore.objects.filter(recurring_source=rc).count()
        resp = self.client.post(reverse('chores:recurring_delete', args=[rc.pk]))
        self.assertRedirects(resp, reverse('chores:recurring_list'))
        # Instances still exist but recurring_source is now NULL
        self.assertEqual(Chore.objects.filter(title='To delete').count(), instance_count)


class EmailNotificationTests(TestCase):
    def test_email_sent_on_new_chore_with_assignee(self):
        member = TeamMember.objects.create(name='Alice', email='alice@example.com')
        Chore.objects.create(
            title='Email test',
            date=date.today(),
            assigned_to=member,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Email test', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['alice@example.com'])

    def test_no_email_without_assignee(self):
        Chore.objects.create(title='No assignee', date=date.today())
        self.assertEqual(len(mail.outbox), 0)

    def test_email_on_reassignment(self):
        member1 = TeamMember.objects.create(name='Alice', email='alice@example.com')
        member2 = TeamMember.objects.create(name='Bob', email='bob@example.com')
        chore = Chore.objects.create(
            title='Reassign test',
            date=date.today(),
            assigned_to=member1,
        )
        mail.outbox.clear()
        chore.assigned_to = member2
        chore.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['bob@example.com'])

    def test_no_email_on_same_assignee_save(self):
        member = TeamMember.objects.create(name='Alice', email='alice@example.com')
        chore = Chore.objects.create(
            title='Same save',
            date=date.today(),
            assigned_to=member,
        )
        mail.outbox.clear()
        chore.title = 'Updated title'
        chore.save()
        self.assertEqual(len(mail.outbox), 0)

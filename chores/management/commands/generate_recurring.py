from django.core.management.base import BaseCommand
from chores.models import RecurringChore
from chores.services import generate_chore_instances


class Command(BaseCommand):
    help = 'Generate biweekly chore instances for all active recurring chores'

    def handle(self, *args, **options):
        recurring = RecurringChore.objects.filter(is_active=True)
        total = 0
        for rc in recurring:
            count = generate_chore_instances(rc)
            if count:
                self.stdout.write(f'  {rc.title}: {count} new instances')
            total += count
        self.stdout.write(self.style.SUCCESS(f'Done. {total} total instances generated.'))

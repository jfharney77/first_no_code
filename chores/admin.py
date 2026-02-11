from django.contrib import admin
from .models import TeamMember, Chore, RecurringChore

admin.site.register(TeamMember)
admin.site.register(Chore)
admin.site.register(RecurringChore)

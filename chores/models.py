from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RecurringChore(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        TeamMember, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='recurring_chores'
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Chore(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    assigned_to = models.ForeignKey(
        TeamMember, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='chores'
    )
    recurring_source = models.ForeignKey(
        RecurringChore, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='instances'
    )
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'title']

    def __str__(self):
        return f"{self.title} ({self.date})"

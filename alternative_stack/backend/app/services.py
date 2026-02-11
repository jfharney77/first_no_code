from datetime import date, timedelta

from sqlalchemy.orm import Session

from .models import Chore, RecurringChore


def generate_chore_instances(db: Session, recurring_chore: RecurringChore, months_ahead: int = 6) -> int:
    """Generate biweekly Chore instances for a RecurringChore.

    Creates instances every 14 days from start_date up to months_ahead months
    from today (or end_date, whichever is sooner). Skips dates that already
    have an instance linked to this recurring chore.

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

    existing_dates = set(
        row[0] for row in db.query(Chore.date)
        .filter(Chore.recurring_source == recurring_chore.id)
        .all()
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
                recurring_source=recurring_chore.id,
            ))
        current += timedelta(days=14)

    if new_chores:
        db.add_all(new_chores)
        db.commit()

    return len(new_chores)


def send_assignment_email(chore: Chore, member_name: str, member_email: str):
    """Print assignment email to console (MVP - swap to real SMTP later)."""
    print("=" * 60)
    print(f"EMAIL TO: {member_email}")
    print(f"SUBJECT: Chore assigned: {chore.title}")
    print(f"")
    print(f"Hi {member_name},")
    print(f"")
    print(f"You have been assigned a chore:")
    print(f"  Title: {chore.title}")
    print(f"  Date: {chore.date}")
    print(f"  Description: {chore.description or '(none)'}")
    print(f"")
    print(f"Please check the office chore calendar for details.")
    print("=" * 60)

from datetime import date, datetime
from pydantic import BaseModel, EmailStr


# ── TeamMember ───────────────────────────────────────────────────────

class TeamMemberCreate(BaseModel):
    name: str
    email: str


class TeamMemberOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Chore ────────────────────────────────────────────────────────────

class ChoreCreate(BaseModel):
    title: str
    description: str = ""
    date: date
    assigned_to: int | None = None


class ChoreUpdate(BaseModel):
    title: str
    description: str = ""
    date: date
    assigned_to: int | None = None


class ChoreOut(BaseModel):
    id: int
    title: str
    description: str
    date: date
    assigned_to: int | None
    assigned_member: TeamMemberOut | None = None
    recurring_source: int | None
    is_completed: bool

    model_config = {"from_attributes": True}


# ── RecurringChore ───────────────────────────────────────────────────

class RecurringChoreCreate(BaseModel):
    title: str
    description: str = ""
    assigned_to: int | None = None
    start_date: date
    end_date: date | None = None
    is_active: bool = True


class RecurringChoreUpdate(BaseModel):
    title: str
    description: str = ""
    assigned_to: int | None = None
    start_date: date
    end_date: date | None = None
    is_active: bool = True


class RecurringChoreOut(BaseModel):
    id: int
    title: str
    description: str
    assigned_to: int | None
    assigned_member: TeamMemberOut | None = None
    start_date: date
    end_date: date | None
    is_active: bool

    model_config = {"from_attributes": True}


# ── Calendar ─────────────────────────────────────────────────────────

class CalendarDay(BaseModel):
    date: date
    chores: list[ChoreOut]
    is_current_month: bool
    is_today: bool


class CalendarResponse(BaseModel):
    year: int
    month: int
    month_name: str
    day_names: list[str]
    weeks: list[list[CalendarDay]]
    prev_year: int
    prev_month: int
    next_year: int
    next_month: int

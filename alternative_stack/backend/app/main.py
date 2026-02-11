import calendar as cal
from datetime import date

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from .database import Base, engine, get_db
from .models import TeamMember, Chore, RecurringChore
from .schemas import (
    TeamMemberCreate, TeamMemberOut,
    ChoreCreate, ChoreUpdate, ChoreOut,
    RecurringChoreCreate, RecurringChoreUpdate, RecurringChoreOut,
    CalendarDay, CalendarResponse,
)
from .services import generate_chore_instances, send_assignment_email

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Office Chores API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Team Members ─────────────────────────────────────────────────────

@app.get("/api/team", response_model=list[TeamMemberOut])
def list_team_members(db: Session = Depends(get_db)):
    return db.query(TeamMember).order_by(TeamMember.name).all()


@app.get("/api/team/{pk}", response_model=TeamMemberOut)
def get_team_member(pk: int, db: Session = Depends(get_db)):
    member = db.query(TeamMember).get(pk)
    if not member:
        raise HTTPException(404, "Team member not found")
    return member


@app.post("/api/team", response_model=TeamMemberOut, status_code=201)
def create_team_member(data: TeamMemberCreate, db: Session = Depends(get_db)):
    member = TeamMember(name=data.name, email=data.email)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@app.put("/api/team/{pk}", response_model=TeamMemberOut)
def update_team_member(pk: int, data: TeamMemberCreate, db: Session = Depends(get_db)):
    member = db.query(TeamMember).get(pk)
    if not member:
        raise HTTPException(404, "Team member not found")
    member.name = data.name
    member.email = data.email
    db.commit()
    db.refresh(member)
    return member


@app.delete("/api/team/{pk}", status_code=204)
def delete_team_member(pk: int, db: Session = Depends(get_db)):
    member = db.query(TeamMember).get(pk)
    if not member:
        raise HTTPException(404, "Team member not found")
    db.delete(member)
    db.commit()


# ── Chores ───────────────────────────────────────────────────────────

@app.get("/api/chores", response_model=list[ChoreOut])
def list_chores(db: Session = Depends(get_db)):
    return (
        db.query(Chore)
        .options(joinedload(Chore.assigned_member))
        .order_by(Chore.date, Chore.title)
        .all()
    )


@app.get("/api/chores/{pk}", response_model=ChoreOut)
def get_chore(pk: int, db: Session = Depends(get_db)):
    chore = (
        db.query(Chore)
        .options(joinedload(Chore.assigned_member))
        .filter(Chore.id == pk)
        .first()
    )
    if not chore:
        raise HTTPException(404, "Chore not found")
    return chore


@app.post("/api/chores", response_model=ChoreOut, status_code=201)
def create_chore(data: ChoreCreate, db: Session = Depends(get_db)):
    chore = Chore(
        title=data.title,
        description=data.description,
        date=data.date,
        assigned_to=data.assigned_to,
    )
    db.add(chore)
    db.commit()
    db.refresh(chore)

    if chore.assigned_to:
        member = db.query(TeamMember).get(chore.assigned_to)
        if member:
            send_assignment_email(chore, member.name, member.email)

    return db.query(Chore).options(joinedload(Chore.assigned_member)).filter(Chore.id == chore.id).first()


@app.put("/api/chores/{pk}", response_model=ChoreOut)
def update_chore(pk: int, data: ChoreUpdate, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(pk)
    if not chore:
        raise HTTPException(404, "Chore not found")

    old_assigned = chore.assigned_to
    chore.title = data.title
    chore.description = data.description
    chore.date = data.date
    chore.assigned_to = data.assigned_to
    db.commit()
    db.refresh(chore)

    if chore.assigned_to and chore.assigned_to != old_assigned:
        member = db.query(TeamMember).get(chore.assigned_to)
        if member:
            send_assignment_email(chore, member.name, member.email)

    return db.query(Chore).options(joinedload(Chore.assigned_member)).filter(Chore.id == chore.id).first()


@app.delete("/api/chores/{pk}", status_code=204)
def delete_chore(pk: int, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(pk)
    if not chore:
        raise HTTPException(404, "Chore not found")
    db.delete(chore)
    db.commit()


@app.post("/api/chores/{pk}/toggle", response_model=ChoreOut)
def toggle_chore(pk: int, db: Session = Depends(get_db)):
    chore = db.query(Chore).get(pk)
    if not chore:
        raise HTTPException(404, "Chore not found")
    chore.is_completed = not chore.is_completed
    db.commit()
    return db.query(Chore).options(joinedload(Chore.assigned_member)).filter(Chore.id == chore.id).first()


# ── Calendar ─────────────────────────────────────────────────────────

@app.get("/api/calendar/{year}/{month}", response_model=CalendarResponse)
def calendar_view(year: int, month: int, db: Session = Depends(get_db)):
    today = date.today()

    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    c = cal.Calendar(firstweekday=6)
    month_days = c.monthdatescalendar(year, month)

    first_day = month_days[0][0]
    last_day = month_days[-1][-1]

    chores = (
        db.query(Chore)
        .options(joinedload(Chore.assigned_member))
        .filter(Chore.date >= first_day, Chore.date <= last_day)
        .order_by(Chore.date, Chore.title)
        .all()
    )

    chore_map: dict[date, list] = {}
    for chore in chores:
        chore_map.setdefault(chore.date, []).append(chore)

    weeks = []
    for week in month_days:
        week_data = []
        for d in week:
            week_data.append(CalendarDay(
                date=d,
                chores=chore_map.get(d, []),
                is_current_month=d.month == month,
                is_today=d == today,
            ))
        weeks.append(week_data)

    prev_month, prev_year = month - 1, year
    if prev_month < 1:
        prev_month, prev_year = 12, year - 1

    next_month, next_year = month + 1, year
    if next_month > 12:
        next_month, next_year = 1, year + 1

    return CalendarResponse(
        year=year,
        month=month,
        month_name=cal.month_name[month],
        day_names=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        weeks=weeks,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
    )


# ── Recurring Chores ─────────────────────────────────────────────────

@app.get("/api/recurring", response_model=list[RecurringChoreOut])
def list_recurring(db: Session = Depends(get_db)):
    return (
        db.query(RecurringChore)
        .options(joinedload(RecurringChore.assigned_member))
        .order_by(RecurringChore.title)
        .all()
    )


@app.get("/api/recurring/{pk}", response_model=RecurringChoreOut)
def get_recurring(pk: int, db: Session = Depends(get_db)):
    rc = (
        db.query(RecurringChore)
        .options(joinedload(RecurringChore.assigned_member))
        .filter(RecurringChore.id == pk)
        .first()
    )
    if not rc:
        raise HTTPException(404, "Recurring chore not found")
    return rc


@app.post("/api/recurring", response_model=RecurringChoreOut, status_code=201)
def create_recurring(data: RecurringChoreCreate, db: Session = Depends(get_db)):
    rc = RecurringChore(
        title=data.title,
        description=data.description,
        assigned_to=data.assigned_to,
        start_date=data.start_date,
        end_date=data.end_date,
        is_active=data.is_active,
    )
    db.add(rc)
    db.commit()
    db.refresh(rc)
    count = generate_chore_instances(db, rc)
    return db.query(RecurringChore).options(joinedload(RecurringChore.assigned_member)).filter(RecurringChore.id == rc.id).first()


@app.put("/api/recurring/{pk}", response_model=RecurringChoreOut)
def update_recurring(pk: int, data: RecurringChoreUpdate, db: Session = Depends(get_db)):
    rc = db.query(RecurringChore).get(pk)
    if not rc:
        raise HTTPException(404, "Recurring chore not found")
    rc.title = data.title
    rc.description = data.description
    rc.assigned_to = data.assigned_to
    rc.start_date = data.start_date
    rc.end_date = data.end_date
    rc.is_active = data.is_active
    db.commit()
    return db.query(RecurringChore).options(joinedload(RecurringChore.assigned_member)).filter(RecurringChore.id == rc.id).first()


@app.delete("/api/recurring/{pk}", status_code=204)
def delete_recurring(pk: int, db: Session = Depends(get_db)):
    rc = db.query(RecurringChore).get(pk)
    if not rc:
        raise HTTPException(404, "Recurring chore not found")
    db.delete(rc)
    db.commit()


@app.post("/api/recurring/{pk}/generate")
def generate_recurring(pk: int, db: Session = Depends(get_db)):
    rc = db.query(RecurringChore).get(pk)
    if not rc:
        raise HTTPException(404, "Recurring chore not found")
    count = generate_chore_instances(db, rc)
    return {"generated": count}

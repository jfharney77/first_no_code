from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chores = relationship("Chore", back_populates="assigned_member")
    recurring_chores = relationship("RecurringChore", back_populates="assigned_member")


class RecurringChore(Base):
    __tablename__ = "recurring_chores"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    assigned_to = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    assigned_member = relationship("TeamMember", back_populates="recurring_chores")
    instances = relationship("Chore", back_populates="recurring_source_rel")


class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    date = Column(Date, nullable=False)
    assigned_to = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    recurring_source = Column(Integer, ForeignKey("recurring_chores.id"), nullable=True)
    is_completed = Column(Boolean, default=False)

    assigned_member = relationship("TeamMember", back_populates="chores")
    recurring_source_rel = relationship("RecurringChore", back_populates="instances")

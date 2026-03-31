from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.database import Base
import enum

class Intent(str, PyEnum):
    PRODUCT_INQUIRY = "product_inquiry"
    PRICING_REQUEST = "pricing_request"
    DEMO_REQUEST = "demo_request"
    FOLLOW_UP_NEEDED = "follow_up_needed"
    NOT_INTERESTED = "not_interested"
    SPAM = "spam"

class Direction(str, PyEnum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class Stage(str, PyEnum):
    INITIAL = "initial"
    FU1 = "fu1"
    FU2 = "fu2"
    CLOSED = "closed"
    CONVERTED = "converted"

class MeetingStatus(str, PyEnum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    company = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    emails = relationship("Email", back_populates="lead")
    conversations = relationship("Conversation", back_populates="lead", uselist=False)
    meetings = relationship("Meeting", back_populates="lead")

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), index=True)
    direction = Column(SQLEnum(Direction), index=True)
    subject = Column(String, index=True)
    body = Column(String)
    intent = Column(SQLEnum(Intent))
    confidence = Column(Float)
    response_body = Column(String)  # Generated reply
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    lead = relationship("Lead", back_populates="emails")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), index=True)
    stage = Column(SQLEnum(Stage), default="initial", index=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    next_fu_at = Column(DateTime(timezone=True))

    lead = relationship("Lead", back_populates="conversations")

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    email_id = Column(Integer, ForeignKey("emails.id"))
    time_slot = Column(DateTime(timezone=True), index=True)
    status = Column(SQLEnum(MeetingStatus), default="proposed")
    calendar_event_id = Column(String)
    timezone = Column(String, default="UTC")

    lead = relationship("Lead", back_populates="meetings")

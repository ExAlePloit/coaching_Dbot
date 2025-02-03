from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .db import Base
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timezone = Column(String, index=True)
    language = Column(String, index=True)
    archived = Column(Boolean, default=False)
    discord_id = Column(String, unique=True, nullable=False)


class GuildConfig(Base):
    __tablename__ = 'guild_config'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    discord_guild = Column(Integer, nullable=False)
    admin_role = Column(Integer, nullable=False)
    mod_role = Column(Integer, nullable=False)
    post_channel = Column(Integer, nullable=False)
    ticket_category = Column(Integer, nullable=False)


class Member(Base):
    __tablename__ = 'members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    discord_id = Column(Integer, unique=True, nullable=False)
    points = Column(Integer, default=0)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    coach_id = Column(Integer, ForeignKey('coaches.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=True)
    button_custom_id = Column(Integer, nullable=False)
    schedule_date = Column(DateTime, nullable=False)
    note = Column(String, nullable=True)
    ticket_channel = Column(Integer, nullable=True)

    coach = relationship('Coach', backref='posts')
    member = relationship('Member', backref='posts')

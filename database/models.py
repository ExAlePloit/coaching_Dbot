import uuid

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timezone = Column(String, index=True)
    language = Column(String, index=True)
    archived = Column(Boolean, default=False)
    discord_id = Column(Integer, unique=True, nullable=False)
    guild_id = Column(UUID, ForeignKey('guild_config.id'), nullable=False)

    guild = relationship("GuildConfig", backref="coaches")


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
    guild_id = Column(UUID, ForeignKey('guild_config.id'), nullable=False)

    guild = relationship("GuildConfig", backref="members")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    coach_id = Column(UUID, ForeignKey('coaches.id'), nullable=False)
    guild_id = Column(UUID, ForeignKey('guild_config.id'), nullable=False)
    member_id = Column(UUID, ForeignKey('members.id'), nullable=True)
    other_info = Column(JSON, nullable=True)
    schedule_date = Column(DateTime, nullable=False)
    ticket_channel = Column(Integer, nullable=True)

    guild = relationship("GuildConfig", backref="posts")
    coach = relationship('Coach', backref='posts')
    member = relationship('Member', backref='posts')

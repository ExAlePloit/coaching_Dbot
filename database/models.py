from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .db import Base
from sqlalchemy.orm import relationship

class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    timezone = Column(String, index=True)
    language = Column(String, index=True)
    archived = Column(Boolean, default=False)
    discord_id = Column(String, unique=True, nullable=False)


class GuildConfig(Base):
    __tablename__ = 'guild_config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_guild_id = Column(String, nullable=False)
    admin_role = Column(String, nullable=False)
    mod_role = Column(String, nullable=False)
    post_channel = Column(String, nullable=False)
    ticket_category = Column(String, nullable=False)

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(String, unique=True, nullable=False)
    points = Column(Integer, default=0)

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coach_id = Column(Integer, ForeignKey('coaches.id'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=True)
    button_custom_id = Column(String, nullable=False)
    schedule_date = Column(DateTime, nullable=False)
    note = Column(String, nullable=True)
    ticket_channel = Column(String, nullable=True)

    coach = relationship('Coach', backref='posts')
    member = relationship('Member', backref='posts')
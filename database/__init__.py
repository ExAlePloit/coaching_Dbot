# database/__init__.py

from .db import SessionLocal
from .crud import DatabaseManager
from .models import Coach, GuildConfig, Member, Post

from .db import Base, engine

Base.metadata.create_all(bind=engine)

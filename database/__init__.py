# database/__init__.py

from .crud import DatabaseManager
from .db import Base, engine
from .db import SessionLocal
from .models import Coach, GuildConfig, Member, Post

Base.metadata.create_all(bind=engine)

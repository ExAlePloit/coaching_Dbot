from datetime import datetime

from .db import SessionLocal
from .models import Coach, GuildConfig, Member, Post


class DatabaseManager:
    def __init__(self):
        self.session = None

    @staticmethod
    def create_or_update_coach(coach_id: str = None, discord_id: int = None, guild_discord_id: id = None,
                               timezone: str = None, language: str = None,
                               archived: bool = None):
        with SessionLocal() as session:

            coach = session.query(Coach).filter(Coach.id == coach_id).first()

            if coach:
                if timezone is not None:
                    coach.timezone = timezone
                if language is not None:
                    coach.language = language
                if archived is not None:
                    coach.archived = archived

                session.commit()
                session.refresh(coach)
                return coach
            else:
                guild_config = DatabaseManager.get_guild_config(guild_discord_id)
                new_coach = Coach(
                    discord_id=discord_id,
                    timezone=timezone,
                    language=language,
                    archived=archived,
                    guild_id=guild_config.id
                )
                session.add(new_coach)
                session.commit()
                session.refresh(new_coach)
                return new_coach

    @staticmethod
    def get_all_coaches():
        with SessionLocal() as session:
            return session.query(Coach).all()

    @staticmethod
    def get_coach_by_id(coach_id: int):
        with SessionLocal() as session:
            return session.query(Coach).filter(Coach.id == coach_id).first()

    @staticmethod
    def get_coach_by_discord(coach_discord_id: int, guild_discord_id: int) -> Coach:
        with SessionLocal() as session:
            return session.query(Coach).join(GuildConfig).filter(Coach.discord_id == coach_discord_id,
                                                                 GuildConfig.discord_guild == guild_discord_id,
                                                                 Coach.guild_id == GuildConfig.id).first()

    @staticmethod
    def delete_coach(coach_id: int) -> bool:
        with SessionLocal() as session:
            coach = session.query(Coach).filter(Coach.id == coach_id).first()
            if coach:
                session.delete(coach)
                session.commit()
                return True
            return False

    @staticmethod
    def create_or_update_guild_config(discord_guild: int, admin_role: int, mod_role: int, post_channel: int,
                                      ticket_category: int):
        with SessionLocal() as session:
            config = session.query(GuildConfig).filter(GuildConfig.discord_guild == discord_guild).first()

            if config:
                config.admin_role = admin_role
                config.mod_role = mod_role
                config.post_channel = post_channel
                config.ticket_category = ticket_category
                session.commit()
                session.refresh(config)
                return config
            else:
                new_config = GuildConfig(
                    discord_guild=discord_guild,
                    admin_role=admin_role,
                    mod_role=mod_role,
                    post_channel=post_channel,
                    ticket_category=ticket_category
                )
                session.add(new_config)
                session.commit()
                session.refresh(new_config)
                return new_config

    @staticmethod
    def get_guild_config(discord_guild_id: int) -> GuildConfig:
        with SessionLocal() as session:
            config = session.query(GuildConfig).filter(GuildConfig.discord_guild == discord_guild_id).first()
            return config

    @staticmethod
    def create_or_update_member(discord_id: id, points: int):
        with SessionLocal() as session:
            member = session.query(Member).filter(Member.discord_id == discord_id).first()

            if member:
                member.points = points
                session.commit()
                session.refresh(member)
                return member
            else:
                new_member = Member(
                    discord_id=discord_id,
                    points=points
                )
                session.add(new_member)
                session.commit()
                session.refresh(new_member)
                return new_member

    @staticmethod
    def get_member_by_discord_id(discord_id: str):
        with SessionLocal() as session:
            return session.query(Member).filter(Member.discord_id == discord_id).first()

    @staticmethod
    def create_post(coach_id: int, member_id: int, button_custom_id: id, schedule_date: datetime, note: str = None):
        with SessionLocal() as session:
            new_post = Post(
                coach_id=coach_id,
                member_id=member_id,
                button_custom_id=button_custom_id,
                schedule_date=schedule_date,
                note=note
            )
            session.add(new_post)
            session.commit()
            session.refresh(new_post)
            return new_post

    @staticmethod
    def update_post(post_id: int, coach_id: int = None, member_id: int = None, button_custom_id: id = None,
                    schedule_date: str = None, note: str = None):
        with SessionLocal() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                if coach_id:
                    post.coach_id = coach_id
                if member_id:
                    post.member_id = member_id
                if button_custom_id:
                    post.button_custom_id = button_custom_id
                if schedule_date:
                    post.schedule_date = schedule_date
                if note is not None:
                    post.note = note
                session.commit()
                session.refresh(post)
                return post
            return None

    @staticmethod
    def delete_post(post_id: int):
        with SessionLocal() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                session.delete(post)
                session.commit()
                return True
            return False

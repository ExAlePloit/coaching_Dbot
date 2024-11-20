from database import *


class DatabaseManager:
    def __init__(self):
        self.session = None

    @staticmethod
    def create_or_update_coach(self, coach_id: int, discord_id: str = None, timezone: str = None, language: str = None,
                               archived: bool = None):
        with SessionLocal() as session:
            coach = session.query(Coach).filter(Coach.id == coach_id).first()

            if coach:
                if discord_id is not None:
                    coach.discord_id = discord_id
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
                new_coach = Coach(
                    discord_id=discord_id,
                    timezone=timezone,
                    language=language,
                    archived=archived
                )
                session.add(new_coach)
                session.commit()
                session.refresh(new_coach)
                return new_coach

    @staticmethod
    def get_all_coaches(self):
        with SessionLocal() as session:
            return session.query(Coach).all()

    @staticmethod
    def get_coach_by_id(self, coach_id: int):
        with SessionLocal() as session:
            return session.query(Coach).filter(Coach.id == coach_id).first()

    @staticmethod
    def delete_coach(self, coach_id: int):
        with SessionLocal() as session:
            coach = session.query(Coach).filter(Coach.id == coach_id).first()
            if coach:
                session.delete(coach)
                session.commit()
                return coach
            return None

    @staticmethod
    def create_or_update_guilt_config(self, discord_guilt_id: str, admin_role: str, mod_role: str, post_channel: str,
                                      ticket_category: str):
        with SessionLocal() as session:
            config = session.query(GuiltConfig).filter(GuiltConfig.discord_guilt_id == discord_guilt_id).first()

            if config:
                config.admin_role = admin_role
                config.mod_role = mod_role
                config.post_channel = post_channel
                config.ticket_category = ticket_category
                session.commit()
                session.refresh(config)
                return config
            else:
                new_config = GuiltConfig(
                    discord_guilt_id=discord_guilt_id,
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
    def get_guilt_config(discord_guilt_id: str):
        with SessionLocal() as session:
            config = session.query(GuiltConfig).filter(GuiltConfig.discord_guilt_id == discord_guilt_id).first()
            return config


    @staticmethod
    def create_or_update_member(discord_id: str, points: int):
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
    def create_post(self, coach_id: int, member_id: int, button_custom_id: str, schedule_date: str, note: str = None):
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
    def update_post(self, post_id: int, coach_id: int = None, member_id: int = None, button_custom_id: str = None,
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
    def delete_post(self, post_id: int):
        with SessionLocal() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                session.delete(post)
                session.commit()
                return True
            return False
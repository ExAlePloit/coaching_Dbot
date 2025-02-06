import uuid
from functools import wraps

from discord import Interaction, Role, TextChannel, CategoryChannel, Member, Embed
from discord import app_commands
from discord.ext import commands

from database import DatabaseManager
from views import CoachingPostView
import dateparser

from .errors import SetupNotDoneError


def guild_initialized():
    async def predicate(interaction: Interaction):
        # if DatabaseManager.get_guild_config(interaction.guild.id):
        #     return True
        raise SetupNotDoneError("Setup is not done.")
    return app_commands.check(predicate)


def check_permission(permission_level):
    def check(func):
        @wraps(func)
        async def inner(self, interaction: Interaction):
            guild_config = DatabaseManager.get_guild_config(interaction.guild.id)
            user_roles = {role.id for role in interaction.user.roles}

            is_coach = DatabaseManager.get_coach_by_discord(
                coach_discord_id=interaction.user.id,
                guild_discord_id=interaction.guild.id
            )
            is_admin = guild_config.admin_role in user_roles
            is_mod = is_admin or (guild_config.mod_role in user_roles)
            is_coach = is_mod or is_coach

            # Check permission hierarchy
            if permission_level == "ADMIN" and is_admin:
                return await func(self, interaction)
            elif permission_level == "MOD" and is_mod:
                return await func(self, interaction)
            elif permission_level == "COACH" and is_coach:
                return await func(self, interaction)

            await interaction.response.send_message(
                "⚠️ Missing permissions!", ephemeral=True)

        return inner

    return check


class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_buttons", description="Show buttons")
    @guild_initialized()
    # @check_permission("COACH")
    async def show_buttons(self, interaction: Interaction):
        """Show buttons"""

        view = CoachingPostView(post_uuid=uuid.uuid4())
        await interaction.response.send_message(f"Coach actions:", view=view)

    @app_commands.command(name="sync", description="Sync commands")
    async def sync(self, interaction: Interaction):
        """Sync commands"""

        self.bot.tree.copy_global_to(guild=interaction.guild)
        synced = await self.bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message(f"Synced {len(synced)} commands.", ephemeral=True)

    @app_commands.command(name="setup_coaching_bot", description="Set up the coaching bot")
    @app_commands.describe(admin_role="Manage the coaches",
                           mod_role="Manage the coaching points of the members",
                           post_channel="Where the member will book coaching",
                           ticket_category="In this category will be created the chats between coaches and members"
                           )
    async def setup_coaching_bot(
            self,
            interaction: Interaction,
            admin_role: Role = None,
            mod_role: Role = None,
            post_channel: TextChannel = None,
            ticket_category: CategoryChannel = None
    ):
        """Set up the coaching bot"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "⚠️ You must have administrator permission!", ephemeral=True)
            return

        if None in [admin_role, mod_role, post_channel, ticket_category]:
            await interaction.response.send_message(
                "⚠️ All parameters must be provided!", ephemeral=True)
            return

        DatabaseManager.create_or_update_guild_config(discord_guild=interaction.guild.id, admin_role=admin_role.id,
                                                      mod_role=mod_role.id, post_channel=post_channel.id,
                                                      ticket_category=ticket_category.id)
        await interaction.response.send_message(f"Setup done.", ephemeral=True)

    @app_commands.command(name="coach", description="Add or edit a coach")
    @app_commands.describe(member="Member to add or edit",
                           timezone="Timezone of the coach",
                           language="Language of the coach",
                           archived="True if the coach is archived, false otherwise"
                           )
    # @guild_initialized
    # @check_permission("ADMIN")
    async def coach(
            self,
            interaction: Interaction,
            member: Member,
            timezone: str = None,
            language: str = None,
            archived: bool = False
    ):
        """Add or edit a coach"""
        DatabaseManager.create_or_update_coach(discord_id=member.id,
                                               guild_discord_id=interaction.guild.id,
                                               timezone=timezone,
                                               language=language,
                                               archived=archived)
        await interaction.response.send_message(f"Coach added.", ephemeral=True)

    @app_commands.command(name="remove_coach", description="Remove a coach")
    @app_commands.describe(member="Coach to remove")
    # @guild_initialized
    # @check_permission("ADMIN")
    async def remove_coach(
            self,
            interaction: Interaction,
            member: Member
    ):
        """Add or edit a coach"""

        coach = DatabaseManager.get_coach_by_discord(member.id, interaction.guild.id)
        if coach:
            DatabaseManager.delete_coach(coach.id)
            await interaction.response.send_message(f"Coach removed.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Coach not found.", ephemeral=True)

    @app_commands.command(name="post_coaching", description="Send a post")
    @app_commands.describe(time="When you want to do the coaching",
                           replay_needed="If you need the replay",
                           gamemode="1s/2s/3s any...",
                           minimum_rank="Minimum rank of the student",
                           maximum_rank="Maximum rank of the student",
                           notes="Any additional information",
                           )
    # @guild_initialized
    # @check_permission("COACH")
    async def post_coaching(
            self,
            interaction: Interaction,
            time: str,
            replay_needed: bool = None,
            gamemode: str = None,
            minimum_rank: str = None,
            maximum_rank: str = None,
            notes: str = None

    ):
        """Add or edit a coach"""
        coach = DatabaseManager.get_coach_by_discord(coach_discord_id=Interaction.user.id,
                                                     guild_discord_id=interaction.guild.id)
        if coach is None:
            await interaction.response.send_message(
                "⚠️ You are not a coach!", ephemeral=True)
            return

        if coach.timezone:
            time += " " + coach.timezone

        time = dateparser.parse(time, settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': True})
        if time is None:
            await interaction.response.send_message(
                "⚠️ Time not valid!", ephemeral=True)
            return

        other_info = {
            "Replay Needed": "Yes" if replay_needed else "No" if replay_needed is not None else None,
            "Gamemode": gamemode,
            "Minimum Rank": minimum_rank,
            "Maximum Rank": maximum_rank,
            "Notes": notes
        }

        embed = Embed(title="📢 COACHING POST", color=0x00BFFF)  # Colore blu Discord
        embed.add_field(name="Hosted by", value=interaction.user.mention, inline=False)
        embed.add_field(name="Scheduled Time", value=f"<t:{int(time.timestamp())}:F>", inline=False)

        for key, value in other_info.items():
            if value is not None:
                embed.add_field(name=key, value=value, inline=False)

        embed.set_footer(text='Click "Claim" to join this coaching')

        await interaction.response.send_message(embed=embed)

        return
        # TODO create the post in the database
        post = DatabaseManager.create_post(coach_id=interaction.user.id, )

        # TODO create the ticket channelTrue
        # TODO create the post message to send

        await interaction.response.send_message(f"Post sent.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(CommandCog(bot))

from functools import wraps
from discord import Interaction, Role, TextChannel, CategoryChannel
from discord import app_commands
from discord.ext import commands
from views import CoachingPostView
import uuid

from database import DatabaseManager


def guild_initialized(func):
    @wraps(func)
    async def inner(self, interaction: Interaction):
        if DatabaseManager.get_guild_config(interaction.guild.id):
            return await func(self, interaction)
        await interaction.response.send_message(
            "⚠️ Setup not done or is missing fields, use /setup_coaching_bot !", ephemeral=True)

    return inner


class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_buttons", description="Show buttons")
    @guild_initialized
    async def show_buttons(self, interaction: Interaction):
        """Show buttons"""

        view = CoachingPostView(post_uuid=uuid.uuid4())
        await interaction.response.send_message(f"Coach actions:", view=view)

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

        if None in [admin_role, mod_role, post_channel, ticket_category]:
            await interaction.response.send_message(
                "⚠️ All parameters must be provided!", ephemeral=True)
            return
        DatabaseManager.create_or_update_guild_config(discord_guild=interaction.guild.id, admin_role=admin_role.id,
                                                      mod_role=mod_role.id, post_channel=post_channel.id,
                                                      ticket_category=ticket_category.id)
        await interaction.response.send_message(f"Setup done.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(CommandCog(bot))

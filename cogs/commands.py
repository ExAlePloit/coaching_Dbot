
from discord import app_commands, Interaction
from discord.ext import commands
from views import ButtonView

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="show_buttons", description="Show buttons")
    async def show_buttons(self, interaction: Interaction):
        """Show buttons"""
        view = ButtonView()
        await interaction.response.send_message("Here are your buttons:", view=view)


async def setup(bot):
    await bot.add_cog(CommandCog(bot))
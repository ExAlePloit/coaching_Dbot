from discord import app_commands
from discord import Interaction

import logging
import logging

import discord
from discord import app_commands
from discord.ext import commands
# Definiamo errori personalizzati
class SetupNotDoneError(app_commands.CheckFailure):
    """Errore personalizzato quando il setup non è completato."""
    pass


class NoPermissionError(app_commands.CheckFailure):
    """Errore personalizzato quando l'utente non ha i permessi necessari."""
    pass
LOGGER: logging.Logger = logging.getLogger(__name__)


class CommandErrors(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.original_command_error = bot.on_command_error
        self.original_app_error = bot.tree.on_error

        bot.on_command_error = self.on_command_error
        bot.tree.on_error = self.on_app_command_error

        self.bot = bot

    async def cog_unload(self) -> None:
        """Load the original error handlers back into the bot when this Cog unloads."""
        self.bot.on_command_error = self.original_command_error
        self.bot.tree.on_error = self.original_app_error

    async def send(
            self,
            content: str,
            /,
            context: commands.Context[commands.Bot] | discord.Interaction[commands.Bot],
            ephemeral: bool = True
    ) -> None:
        """Simple generic method for sending a response.

        Parameters
        ----------
        content: str
            The content to send in the response.
        context: commands.Context | discord.Interaction
            The context or interaction surrounding the command or app command.
        ephemeral: bool
            Optional bool indicating whether the repsonse should attempted to be sent ephemerally. Defaults to True.
        """
        if isinstance(context, commands.Context):
            send = context.send
        else:
            send = context.response.send_message if not context.response.is_done() else context.followup.send

        try:
            await send(content=content, ephemeral=ephemeral)
        except discord.HTTPException as e:
            msg = f'Ignoring HTTPException in %r for %r: %s\n\n'
            LOGGER.error(msg, self.send.__name__, self.__class__.__name__, e, exc_info=e)

    async def on_command_error(self, ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
        """Prefix command error handler."""
        if ctx.command and ctx.command.has_error_handler():
            return

        elif ctx.cog and ctx.cog.has_error_handler():
            return

        error = getattr(error, 'original', error)
        ignored = (commands.CommandNotFound, commands.NotOwner)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            await self.send("This command can not be used in Private Messages.", context=ctx)
        elif isinstance(error, commands.DisabledCommand):
            await self.send("This command has been disabled by the owner.", context=ctx)
        else:
            LOGGER.error("Ignoring exception in command %s", ctx.command, exc_info=error)

    async def on_app_command_error(
            self,
            interaction: discord.Interaction[commands.Bot],
            error: app_commands.AppCommandError,
    ) -> None:
        """AppCommand error handler."""

        print("tree error:", error, type(error), isinstance(error, SetupNotDoneError), error.__class__,
              getattr(error, "original", None), isinstance(error, app_commands.CheckFailure))
        command = interaction.command

        if command is None:
            LOGGER.error("Ignoring exception in command tree", exc_info=error)
            return

        if command.on_error:
            return
        if isinstance(error, SetupNotDoneError):
            await self.send(f"⚠️ Setup not done or missing fields, use `/setup_coaching_bot`!",
                            context=interaction)
        if isinstance(error, app_commands.CommandOnCooldown):
            retry_after = error.cooldown.get_retry_after()
            await self.send(f"This command is on cooldown. Try again in {retry_after:.2f} seconds...",
                            context=interaction)
        else:
            await self.send(f"**This application received an unhandled exception:**\n\n{error}", context=interaction)
            LOGGER.error('Ignoring exception in command %r', command.name, exc_info=error)


async def setup(bot):
    await bot.add_cog(CommandErrors(bot))
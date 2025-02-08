import nextcord
from nextcord.ext import  application_checks
from bot.settings import settings, Setting
from bot import util
import logging

logger = logging.getLogger(__name__)


def config_embed(name : str, value : str) -> nextcord.Embed:
    embed = nextcord.Embed(
        title="Config Changed",
        description=f"set {name} to {value}",
        color=nextcord.Color.green()
    )

    return embed

def setup(bot):
    @bot.slash_command(description="Config Commands")
    @application_checks.check(util.has_permissions)
    async def config(self):
        pass

    for setting in settings:
        def create_command(setting : Setting):
            @application_checks.check(util.has_permissions)
            @config.subcommand(name=setting.name, description=setting.description)
            async def command(
                    interaction: nextcord.Interaction,
                    value: nextcord.TextChannel if setting.value_type == nextcord.TextChannel else bool
            ):
                logger.info(f"received config command, setting {setting.name} to {value} ({type(value)})")
                setting.set(value)
                await interaction.send(embed=config_embed(setting.name, value), ephemeral=True)
        create_command(setting)
import nextcord
from nextcord.ext import commands, application_checks
from nextcord.types import embed

from bot.settings import settings
from bot import util

def config_embed(name : str, value : str) -> nextcord.Embed:
    embed = nextcord.Embed(
        title="Config Changed",
        description=f"set {name} to {value}",
        color=nextcord.Color.green()
    )

    return embed

def setup(bot):
    @bot.slash_command()
    async def config(self, ctx):
        pass

    for setting in settings:
        @application_checks.check(util.has_permissions)
        @config.subcommand(name=setting.name, description=setting.description)
        async def command(
                ctx: nextcord.Interaction,
                value: nextcord.TextChannel if setting.value_type == nextcord.TextChannel else bool
        ):
            setting.set(value)
            await ctx.send(embed=config_embed(setting.name, value),ephemeral=True)
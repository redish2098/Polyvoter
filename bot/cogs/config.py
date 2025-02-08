import nextcord
from nextcord.ext import  application_checks
from bot.settings import settings, Setting
from bot import util



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
                    value:
                    nextcord.TextChannel if setting.value_type == nextcord.TextChannel
                    else nextcord.Role if setting.value_type == nextcord.Role
                    else bool
            ):
                setting.set(value)
                await interaction.send(embed=util.success_embed(f"set {setting.name} to {value}"), ephemeral=True)
        create_command(setting)
import dotenv
import nextcord
from nextcord.ext import commands
import os
from bot.database import schema
from bot import util


intents = nextcord.Intents.all()
bot = commands.Bot(
    intents=intents,
)

dotenv.load_dotenv()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    for guild in bot.guilds:
        print(f"{guild.name} (id:{str(guild.id)})")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error : Exception):
    print(f"Error: {error}")
    if isinstance(error, nextcord.errors.ApplicationCheckFailure):
        embed = util.error_embed("You don't have permission to use this command!")
    else:
        embed = util.error_embed("An error occurred running this command")

    if embed is not None:
        if not interaction.response.is_done():
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.edit_original_message(embed=embed)

    raise error


schema.setup()

bot.load_extension("bot.cogs.config")
bot.load_extension("bot.cogs.moderation")
bot.load_extension("bot.cogs.submissions")
bot.load_extension("bot.cogs.voting")
bot.load_extension("bot.cogs.leaderboard")

@bot.slash_command(name="help", description="Shows a list of available commands")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="Available Commands", color=nextcord.Color.blue())
    for cmd in bot.get_all_application_commands():
        if any(
                not(
                        check.__name__ == util.has_permissions.__name__ and util.has_permissions(interaction)
                )
                for check in cmd.checks
        ):
            continue
        embed.add_field(name=f"/{cmd.name}", value=cmd.description or "No description available.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)



bot.run(os.environ["DISCORD_TOKEN"])
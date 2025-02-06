import dotenv
import nextcord
from nextcord.ext import commands, application_checks
import os

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)


dotenv.load_dotenv()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    for guild in bot.guilds:
        print(f"{guild.name} (id:{str(guild.id)})")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    print(f"Error: {error}")
    if isinstance(error, nextcord.errors.ApplicationCheckFailure):
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred!", ephemeral=True)

bot.load_extension("cogs.config")
bot.run(os.environ["DISCORD_TOKEN"])
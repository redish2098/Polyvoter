import os

import nextcord
from bot.settings import get_setting,Settings

reaction_emojis = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5}

def has_permissions(interaction: nextcord.Interaction) -> bool:
    if int(os.environ["OWNER"]) ==  interaction.user.id:
        return True

    if(any(
            role.id == get_setting(Settings.MOD_ROLE).get() or role.permissions.administrator
            for role in interaction.user.roles
    )):
        return True
    return False

def success_embed(message: str, title : str = "Success!", color: nextcord.Color = nextcord.Color.green()) -> nextcord.Embed:
    return nextcord.Embed(title=title, description=message, color=color)

def error_embed(message: str, title : str = "Error :(", color: nextcord.Color = nextcord.Color.red()) -> nextcord.Embed:
    return nextcord.Embed(title=title, description=message, color=color)
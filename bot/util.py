import os

import nextcord
from bot.settings import get_setting,Settings

reaction_emojis = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5}

def is_owner(interaction : nextcord.Interaction) -> bool:
    return int(os.environ["OWNER"]) ==  interaction.user.id

def has_permissions(interaction: nextcord.Interaction) -> bool:
    if int(os.environ["OWNER"]) ==  interaction.user.id:
        return True

    if(any(
            role.id == get_setting(Settings.MOD_ROLE).get() or role.permissions.administrator
            for role in interaction.user.roles
    )):
        return True
    return False

def success_embed(message: str) -> nextcord.Embed:
    return nextcord.Embed(title= "Success!", description=message, color=nextcord.Color.green())

def error_embed(message: str) -> nextcord.Embed:
    return nextcord.Embed(title="Error :(", description=message, color=nextcord.Color.red())

def generic_embed(message: str, title : str, color: nextcord.Color) -> nextcord.Embed:
    return nextcord.Embed(title=title, description=message, color=color)
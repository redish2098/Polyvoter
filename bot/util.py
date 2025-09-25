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

role_must_include = [
    425512059904589834, #rider
    427239028577009664, #raft
    427239027368919041, #amphibian
    705114770361155694, #hexapod
    427239029747089418, #mooni
    705115347862159380, #phychi
    427239026542510090, #archer
    427239025498128384, #ice archer
    427239024348889089, #defender
    556228432778756117, #scout
    705115346834817085, #catapult
    427239021903609857, #polytaur
    427239022985740291, #swordsman
    705114778099777627, #tridention
    425511644261515265, #battle sled
    425511634891440130, #knight
    556228668448309283, #doomux
    425511637567406110, #ice fortress
    425511639467556865, #bomber
    837851362111914014, #juggernaut
    425511642206437376, #mind bender
    837851447457873990, #shaman
    705114778892501055, #giant
    837851617800880178, #crab
    500442104825118740, #centipede
    837851688760770601, #gaami
    837851752979496981, #dragon egg
    837851830838624286, #baby dragon
    837851913139650581, #dragon
    425511626158899200, #nature bunny
]

def can_vote(member : nextcord.Member) -> bool:
    if member is None:
        return False
    allowed = False
    for role in member.roles:
        if role.id in role_must_include:
            allowed = True
            break
    return allowed
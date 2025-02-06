import os

import nextcord

reaction_emojis = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5}

def has_permissions(interaction: nextcord.Interaction) -> bool:
    if int(os.environ["OWNER"]) ==  interaction.user.id:
        return True
import nextcord
from nextcord.ext import commands
from bot.database import contest_lifecycle
import itertools
from bot.settings import get_setting,Settings
import hashlib
import json


class Leaderboard(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.leaderboard_hash = None
        self.leaderboard = None

    @staticmethod
    def hash_leaderboard(leaderboard : dict[int,tuple[float,int,int]]):
        return hashlib.md5(json.dumps(leaderboard).encode()).digest()

    async def count_leaderboard(self) -> nextcord.Embed:
        votes = contest_lifecycle.get_votes(10)
        embed = nextcord.Embed(
            title="Leaderboard",
            description="Leaderboard of top 10 submissions",
        )
        new_hash = self.hash_leaderboard(votes)
        if self.leaderboard_hash != new_hash or self.leaderboard is None:
            pos = 1
            for i, (k, v) in enumerate(votes.items()):
                channel = await self.bot.fetch_channel(get_setting(Settings.CHANNEL).get())
                message = await channel.fetch_message(k)
                embed.add_field(
                    name=f"{pos}) {message.author.display_name}",
                    value=f"Average: {v[0]}\nTotal: {v[1]}\nVotes: {v[2]}\n[Jump to submission]({message.jump_url})",
                    inline=False,
                )
                pos += 1
            self.leaderboard = embed
            self.leaderboard_hash = new_hash
        else:
            embed = self.leaderboard
        return embed

    @nextcord.slash_command(description="Creates a leaderboard of top 10 submissions")
    async def leaderboard(self, interaction : nextcord.Interaction):
        embed = await self.count_leaderboard()
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.leaderboard = Leaderboard(bot)
    bot.add_cog(bot.leaderboard)

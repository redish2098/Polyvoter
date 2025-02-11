import nextcord
from nextcord.ext import commands
from bot.settings import Settings,get_setting
from bot import util
from bot.database import contest_lifecycle
import logging

logger = logging.getLogger(__name__)

class Voting(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_event: nextcord.RawReactionActionEvent):
        if (reaction_event.member.bot or
                not get_setting(Settings.ENABLED).get() or
                not reaction_event.channel_id == get_setting(Settings.CHANNEL).get()):
            return

        channel = await self.bot.fetch_channel(reaction_event.channel_id)
        message = await channel.fetch_message(reaction_event.message_id)
        if not get_setting(Settings.VOTING).get():
            await message.remove_reaction(reaction_event.emoji, reaction_event.member)
            return

        if reaction_event.emoji.name in util.reaction_emojis:
            contest_lifecycle.set_vote(reaction_event.user_id, reaction_event.message_id, util.reaction_emojis[reaction_event.emoji.name])
            logger.info(f"user {reaction_event.user_id} voted {util.reaction_emojis[reaction_event.emoji.name]} on {reaction_event.message_id}")
            for emoji in util.reaction_emojis:
                if reaction_event.emoji.name == emoji:
                    continue
                await message.remove_reaction(emoji, reaction_event.member)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction_event: nextcord.RawReactionActionEvent):
        guild = await self.bot.fetch_guild(reaction_event.guild_id)
        member = await guild.fetch_member(reaction_event.user_id)

        if member.bot or not get_setting(Settings.ENABLED).get() or not get_setting(Settings.VOTING).get():
            return

        if reaction_event.emoji.name in util.reaction_emojis:
            contest_lifecycle.remove_vote(reaction_event.user_id, reaction_event.message_id, util.reaction_emojis[reaction_event.emoji.name])
            logger.info(f"user {reaction_event.user_id} removed vote {util.reaction_emojis[reaction_event.emoji.name]} on {reaction_event.message_id}")

def setup(bot):
    bot.add_cog(Voting(bot))
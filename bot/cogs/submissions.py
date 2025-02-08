import nextcord
from nextcord.ext import commands
from bot import settings
from bot.settings import Settings
from bot import util
from bot.database import contest_lifecycle

class Submissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self , message : nextcord.Message):
        if (not settings.get_setting(Settings.ENABLED).get() or
                message.channel.id != settings.get_setting(Settings.CHANNEL).get() or
                message.author.bot):
            return
        if not settings.get_setting(Settings.SUBMITTING).get():
            await message.author.create_dm()
            await message.author.dm_channel.send("submitting is currently not enabled, sending submission:")
            await message.forward(message.author.dm_channel)
            await message.delete()

        else:
            async for message_history in message.channel.history(limit=None):
                if (
                        message.id != message_history.id
                        and message_history.author.id == message.author.id
                ):
                    await message.author.send(
                        "You can only submit once per event, sending submission:"
                    )
                    await message.author.create_dm()
                    await message.forward(message.author.dm_channel)
                    await message.delete()
                    break
            else:
                for e in util.reaction_emojis:
                    await message.add_reaction(e)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, message : nextcord.RawMessageDeleteEvent):
        if (not settings.get_setting(Settings.ENABLED).get() or
                message.channel_id != settings.get_setting(Settings.CHANNEL).get()):
            return

        contest_lifecycle.delete_submission_votes(message.message_id)


def setup(bot):
    bot.add_cog(Submissions(bot))
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks
from bot import util, settings
from bot.database import contest_lifecycle
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Moderation commands")
    @application_checks.check(util.has_permissions)
    async def moderation(self, interaction: nextcord.Interaction):
        pass

    @moderation.subcommand(description="Start a contest")
    @application_checks.check(util.has_permissions)
    async def start_contest(self, interaction: nextcord.Interaction, channel: Optional[nextcord.TextChannel] = SlashOption(required=False)):
        contest_lifecycle.new_contest()
        settings.get_setting(settings.Settings.VOTING).set(False)
        settings.get_setting(settings.Settings.SUBMITTING).set(True)
        if channel is not None:
            settings.get_setting(settings.Settings.CHANNEL).set(channel)
        await interaction.response.send_message(embed=util.success_embed("Contest has been started!"), ephemeral=True)

    @moderation.subcommand(description="End a contest")
    @application_checks.check(util.has_permissions)
    async def end_contest(self, interaction: nextcord.Interaction):
        settings.get_setting(settings.Settings.VOTING).set(False)
        settings.get_setting(settings.Settings.SUBMITTING).set(False)

        # recount leaderboard
        # send to website

        await interaction.response.send_message(embed=util.success_embed("Contest has been ended!"), ephemeral=True)

    @moderation.subcommand(description="Start voting for a contest and end submissions")
    @application_checks.check(util.has_permissions)
    async def start_voting(self, interaction: nextcord.Interaction):
        settings.get_setting(settings.Settings.VOTING).set(True)
        settings.get_setting(settings.Settings.SUBMITTING).set(False)

        checked = 0
        response_message = await interaction.response.send_message(embed=util.success_embed(f"Starting Contest {checked} submission(s) checked","checking...",color=nextcord.Color.orange()), ephemeral=True)

        channel = await self.bot.fetch_channel(settings.get_setting(settings.Settings.CHANNEL).get())
        async for message in channel.history(limit=200):
            if not message.author.bot:
                for e in util.reaction_emojis:
                    await message.add_reaction(e)

                checked += 1
                await response_message.edit(embed=util.success_embed(f"Starting Contest {checked} submission(s) checked","checking...",color=nextcord.Color.orange()))

        await response_message.edit(embed=util.success_embed("Contest has started voting period and submitting is now unallowed"))

    @moderation.subcommand(description="Delete all votes from a user")
    @application_checks.check(util.has_permissions)
    async def delete_votes(self, interaction: nextcord.Interaction, user: nextcord.User):
        contest_lifecycle.delete_user_votes(user.id)

        channel = await self.bot.fetch_channel(settings.get_setting(settings.Settings.CHANNEL).get())
        async for message in channel.history(limit=200):
            if not message.author.bot:
                for e in util.reaction_emojis:
                    await message.remove_reaction(e,user)

        await interaction.response.send_message(embed=util.success_embed(f"votes from {user.name} have been removed"), ephemeral=True)

    @moderation.subcommand(description="announce a message and/or image in the contest channel")
    @application_checks.check(util.has_permissions)
    async def announce(
            self,
            interaction: nextcord.Interaction,
            message: str = nextcord.SlashOption(required=False),
            image: nextcord.Attachment = nextcord.SlashOption(required=False)
    ):
        channel = await self.bot.fetch_channel(settings.get_setting(settings.Settings.CHANNEL).get())
        if message is None and image is None:
            response_message = "You must have a message or an image to send"
        elif message is None:
            await channel.send(f"{image.url}")
            response_message = "Message sent"
        elif image == None:
            await channel.send(message)
            response_message = "Message sent"
        else:
            await channel.send(message + f"\n{image.url}")
            response_message = "Message sent"

        await interaction.send(embed=util.success_embed(response_message), ephemeral=True)





def setup(bot):
    bot.add_cog(Moderation(bot))
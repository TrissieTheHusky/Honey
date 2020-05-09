from datetime import datetime as dt

import discord

from cogs import utils


class MessageHandler(utils.Cog):

    @utils.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        """Logs edited messages"""

        # Filter
        if after.guild is None:
            return
        if before.content == after.content:
            return
        if not before.content or not after.content:
            return
        if after.author.bot:
            return

        # Create embed
        with utils.Embed(colour=0x0000ff) as embed:
            embed.set_author_to_user(user=after.author)
            embed.description = f"[Message edited]({after.jump_url}) in {after.channel.mention}"
            before_content = before.content
            if len(before.content) > 1000:
                before_content = before.content[:1000] + '...'
            after_content = after.content
            if len(after.content) > 1000:
                after_content = after.content[:1000] + '...'
            embed.add_field(name="Old Message", value=before_content, inline=False)
            embed.add_field(name="New Message", value=after_content, inline=False)
            embed.timestamp = after.edited_at

        # Get channel
        channel_id = self.bot.guild_settings[after.guild.id].get("edited_message_modlog_channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        # Send log
        try:
            m = await channel.send(embed=embed)
            self.logger.info(f"Logging edited message (G{m.guild.id}/C{m.channel.id})")
        except discord.Forbidden:
            pass

    @utils.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        """Logs edited messages"""

        # Filter
        if message.guild is None:
            return
        if not message.content:
            return
        if message.author.bot:
            return

        # Create embed
        with utils.Embed(colour=0xff0000) as embed:
            embed.set_author_to_user(user=message.author)
            embed.description = f"Message deleted in {message.channel.mention}"
            if len(message.content) > 1000:
                embed.add_field(name="Message", value=message.content[:1000] + '...', inline=False)
            else:
                embed.add_field(name="Message", value=message.content, inline=False)
            embed.timestamp = dt.utcnow()

        # Get channel
        channel_id = self.bot.guild_settings[message.guild.id].get("edited_message_modlog_channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return

        # Send log
        try:
            m = await channel.send(embed=embed)
            self.logger.info(f"Logging deleted message (G{m.guild.id}/C{m.channel.id})")
        except discord.Forbidden:
            pass


def setup(bot:utils.Bot):
    x = MessageHandler(bot)
    bot.add_cog(x)
import discord
import json
import logging
from datetime import datetime, timezone, timedelta

class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self.load_config()
        self.logger = logging.getLogger('bot')

    def load_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.guild:
            await self.log_message(message)

    async def on_message_edit(self, before, after):
        if after.guild:
            await self.log_message_edit(before, after)

    async def on_message_delete(self, message):
        if message.guild:
            await self.log_message_delete(message)

    async def log_message(self, message):
        log_message = self.format_log_message(message, "新規メッセージ")
        await self.send_log(message, log_message)

    async def log_message_edit(self, before, after):
        log_message = f"メッセージ編集:\n"
        log_message += self.format_log_message(before, "編集前")
        log_message += "\n"
        log_message += self.format_log_message(after, "編集後")
        await self.send_log(after, log_message)

    async def log_message_delete(self, message):
        log_message = self.format_log_message(message, "削除されたメッセージ")
        await self.send_log(message, log_message)

    def format_log_message(self, message, event_type):
        log_message = f"----- {event_type} -----\n"
        log_message += f"鯖名: {message.guild.name}\n"
        log_message += f"チャンネル: {message.channel.name}\n"
        log_message += f"発言者: {message.author}\n"
        log_message += f"時刻: {self.format_time(message.created_at)}\n"
        log_message += f"内容: {message.content}\n"

        if message.attachments:
            for attachment in message.attachments:
                log_message += f"画像URL: {attachment.url}\n"
        log_message += "--------------------------"
        return log_message

    async def send_log(self, message, log_message):
        if str(message.channel.id) in self.config["special_log_channels"]:
            special_log_channel = self.get_channel(self.config["special_log_channels"][str(message.channel.id)])
            if special_log_channel:
                await self.safe_send(special_log_channel, log_message)

        if str(message.guild.id) in self.config["server_log_channels"]:
            server_log_channel = self.get_channel(self.config["server_log_channels"][str(message.guild.id)])
            if server_log_channel:
                await self.safe_send(server_log_channel, log_message)

    async def safe_send(self, channel, content):
        try:
            await channel.send(content)
        except discord.errors.HTTPException as e:
            self.logger.error(f"Error sending message to channel {channel.id}: {e}")

    def format_time(self, time):
        jst = timezone(timedelta(hours=9))
        return time.astimezone(jst).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot = MyBot()
    bot.run(bot.config["token"])

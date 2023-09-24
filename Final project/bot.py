import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as{0}!', self.user)
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello World!')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('Discord Bot Token')

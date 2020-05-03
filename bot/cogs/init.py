import discord
from discord.ext import commands
from datetime import datetime
from settings.db_commands import connect

class Init(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(datetime.now().strftime('\n%d/%m/%Y - %H:%M:%S\n'))

        connect()
        
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("?help para ajuda"))
        print('[*] Bot online')

def setup(client):
    client.add_cog(Init(client))
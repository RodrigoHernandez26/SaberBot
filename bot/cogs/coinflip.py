import discord
from discord.ext import commands
import secrets

class Coinflip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        number = secrets.choice([1, 2])

        if number == 1:
             resultado = 'Coroa!'

        else:
            resultado = 'Cara!'

        await ctx.channel.send(f'<@!{ctx.author.id}> | {resultado}')

def setup(client):
    client.add_cog(Coinflip(client))
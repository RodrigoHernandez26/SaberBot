import discord
from discord.ext import commands
from misc.embeds import help_embed

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed = help_embed())

def setup(client):
    client.add_cog(Help(client))
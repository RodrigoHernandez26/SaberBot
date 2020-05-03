import discord
from discord.ext import commands
from misc.embeds import pontos_vazio, pontos_lista
from settings.db_commands import mysql_command

class Pontos(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pontos(self, ctx):

        data = mysql_command(f"select nome, pontos from pnts where server = {ctx.guild.id} order by pontos desc", True)

        if len(data) == 0:
            await ctx.channel.send(embed = pontos_vazio())
        else:
            await ctx.channel.send(embed = pontos_lista(data))
   
def setup(client):
    client.add_cog(Pontos(client))
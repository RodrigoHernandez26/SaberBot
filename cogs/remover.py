import discord
from discord.ext import commands
from misc.embeds import remover_nome
from misc.embeds_user_error import erro
from settings.db_commands import mysql_command

class Remover(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remover(self, ctx, msg):

        nome = msg.lower().capitalize()

        data = mysql_command(f"select * from pnts where nome = '{nome}' and server = {ctx.guild.id}", True)

        if len(data) != 0:
            mysql_command(f"delete from pnts where id_pontos = {data[0]['id_pontos']} and server = {ctx.guild.id}")

            await ctx.channel.send(embed = remover_nome(nome))
            return
        
        await ctx.channel.send(embed = erro(nome))

def setup(client):
    client.add_cog(Remover(client))

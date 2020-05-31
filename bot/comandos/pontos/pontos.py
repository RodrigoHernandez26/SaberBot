import discord
from discord.ext import commands
from misc.embeds import pontos_vazio, pontos_lista
from settings.db_commands import mysql_command

async def pontos(ctx, msg, client):

    data = mysql_command(f"select nome, pontos from pnts where server = {ctx.guild.id} order by pontos desc", True)

    if len(data) == 0:
        await ctx.channel.send(embed = pontos_vazio())
    else:
        await ctx.channel.send(embed = pontos_lista(data))

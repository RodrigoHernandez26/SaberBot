import discord
from discord.ext import commands
from discord.ext.commands import UserInputError
from misc.embeds import novo_repetido, novo_adicionado
from misc.embeds_user_error import novo_erro
from settings.db_commands import mysql_command

async def novo(ctx, msg, client):

    nome = msg[0].lower().capitalize()

    data = mysql_command(f'select nome from pnts where nome = "{nome}" and server = {ctx.guild.id}', True)
    
    if len(data) != 0:
        await ctx.channel.send(embed = novo_repetido(nome))
    
    else:
        mysql_command(f'insert into pnts (nome, server) value ("{nome}", {ctx.guild.id})')
        await ctx.channel.send(embed = novo_adicionado(nome))
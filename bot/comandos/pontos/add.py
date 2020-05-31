import discord
import yaml
from discord.ext import commands
from discord.ext.commands import UserInputError
from misc.embeds import add_singular, add_plural, add_limite
from misc.embeds_user_error import add_erro, erro
from settings.db_commands import mysql_command

async def add(ctx, msg, client):

    with open('./bot/settings/settings.yaml', 'r') as f: settings = yaml.load(f, Loader= yaml.FullLoader)

    nome  = msg[1].lower().capitalize()

    try:
        ponto = int(msg[0])
        assert int(ponto) > 0

        if int(ponto) > settings['LIM_ADD']: 
            await ctx.channel.send(embed = add_limite())
            return

    except Exception:
        await ctx.channel.send(embed = add_erro())
        return

    try:
        data = mysql_command(f"select * from pnts where nome = '{nome}' and server = {ctx.guild.id}", True)[0]
    except Exception:
        await ctx.channel.send(embed = erro(nome))
        return
    
    data = mysql_command(f"select * from pnts where nome = '{nome}' and server = {ctx.guild.id}", True)
    finalponto = int(data[0]['pontos']) + int(ponto)
    mysql_command(f"update pnts set pontos = {finalponto} where id_pontos = {data[0]['id_pontos']} and server = {ctx.guild.id}")

    if int(ponto) == 1:
        await ctx.channel.send(embed = add_singular(nome))
        return
        
    else:
        await ctx.channel.send(embed = add_plural(nome, ponto))
        return
        
    await ctx.channel.send(embed = add_erro())
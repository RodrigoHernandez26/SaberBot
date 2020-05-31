import discord
from discord.ext import commands
from discord.ext.commands import UserInputError
from misc.embeds import retirar_singular, retirar_plural
from misc.embeds_user_error import retirar_erro, erro
from settings.db_commands import mysql_command

async def retirar(ctx, msg, client):

    try:
        ponto = int(msg[0])
        assert int(ponto) > 0
    
    except Exception:
        await ctx.channel.send(embed = retirar_erro())
        return

    nome = msg[1].lower().capitalize()

    data = mysql_command(f"select * from pnts where nome = '{nome}' and server = {ctx.guild.id}", True)

    if len(data) != 0:

        if int(data[0]['pontos']) - int(ponto) >= 0:
            finalponto = int(data[0]['pontos']) - int(ponto)
            mysql_command(f"update pnts set pontos = {finalponto} where id_pontos = {data[0]['id_pontos']} and server = {ctx.guild.id}")

            if int(ponto) == 1:
                await ctx.channel.send(embed = retirar_singular(nome))
                return
                
            else:
                await ctx.channel.send(embed = retirar_plural())
                return

        else:
            await ctx.channel.send(embed = retirar_erro())
            return
    
    await ctx.channel.send(embed = erro(nome))

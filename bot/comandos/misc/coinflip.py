import discord
from discord.ext import commands
import secrets

async def coinflip(ctx, msg, client):
    number = secrets.choice([1, 2])

    if number == 1:
            resultado = 'Coroa!'

    else:
        resultado = 'Cara!'

    await ctx.channel.send(f'<@!{ctx.author.id}> | {resultado}')
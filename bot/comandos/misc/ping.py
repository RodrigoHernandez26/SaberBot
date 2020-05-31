import discord
from discord.ext import commands
from settings.db_commands import mysql_command

async def ping(ctx, msg, client):

    ping_embed = discord.Embed(
        title = f'⌛️ {round(client.latency * 1000)} ms',
        color = 0x22a7f0
    )
    await ctx.channel.send(embed = ping_embed)
    mysql_command(f"update status_api set disc = {client.latency * 1000} where id = 1")
import discord
from discord.ext import commands
from misc.embeds import help_embed

async def help(ctx, msg, client):
    await ctx.channel.send(embed = help_embed())
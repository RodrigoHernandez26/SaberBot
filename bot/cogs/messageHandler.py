import discord
from discord.ext import commands
from settings.db_commands import mysql_command
from moderation.flood import Flood
from moderation.badwords import Badword
from moderation.spamcaps import SpamCaps
from moderation.link import Link

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        
        if ctx.author.bot:
            return
        
        try:
            data = mysql_command(f"select id_role from adm_roles where server = {ctx.guild.id}", True)[0]['id_role']
        except Exception:
            data = 0

        for role in ctx.author.roles:
            if role.id == data:
                return

        await Flood.flood(ctx)
        await Badword.verifyBadWords(ctx)
        await SpamCaps.spamcaps(ctx)
        await Link.link(ctx)
        
def setup(client):
    client.add_cog(Moderation(client))
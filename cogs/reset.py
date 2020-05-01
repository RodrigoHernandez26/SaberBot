import discord
from discord.ext import commands
from misc.embeds import reset_true, reset_false, reset_fail, reset_none
from settings.db_commands import mysql_command

class Reset(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reset(self, ctx):
        pnts = mysql_command("select * from pnts", True)
        try:
            role_perm = mysql_command(f"select * from reset_roles where server = {ctx.guild.id}", True)[0]['id_role']

        except Exception:
            await ctx.channel.send(embed = reset_none())
            return
        
        if len(pnts) != 0:
            for role in ctx.author.roles:
                if role_perm == role.id:
                    mysql_command(f"delete from pnts where server = {ctx.guild.id}")
                    await ctx.channel.send(embed = reset_true())
                    return

            await ctx.channel.send(embed = reset_false())
        else:
            await ctx.channel.send(embed = reset_fail())

def setup(client):
    client.add_cog(Reset(client))
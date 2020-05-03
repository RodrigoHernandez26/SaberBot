import discord
from discord.ext import commands
from settings.db_commands import mysql_command
from misc.embeds import setadm_erro, setadm_alterado, setadm_neg

class SetAdm(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def setadm(self, ctx, role):
        if ctx.author.id == ctx.guild.owner.id:
            try:
                role = int(role)
                role_obj = ctx.guild.get_role(role)
                assert role_obj != None

            except Exception:
                try:
                    role = role[3:-1]
                    role = int(role)
                    role_obj = ctx.guild.get_role(role)
                    assert role_obj != None

                except Exception:
                    await ctx.channel.send(embed = setadm_erro())
                    return

            try:
                data = mysql_command(f'select * from reset_roles where server = {ctx.guild.id}', True)[0]
                mysql_command(f'update reset_roles set id_role = {role} where server = {ctx.guild.id}')

            except Exception:
                mysql_command(f'insert into reset_roles (server, id_role) value ({ctx.guild.id}, {role})')

            await ctx.channel.send(embed = setadm_alterado(role_obj))

        else:
            await ctx.channel.send(embed = setadm_neg(ctx.guild.owner))

def setup(client):
    client.add_cog(SetAdm(client))
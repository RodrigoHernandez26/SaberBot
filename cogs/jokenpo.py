import discord
from discord.ext import commands
from discord.ext.commands import UserInputError
from misc.embeds_user_error import jokenpo_erro
from misc.embeds import jokenpo_bot, jokenpo_user, jokenpo_empate
import secrets

class Jokenpo(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_command_error(self, ctx, error):
        if isinstance(error, UserInputError):
            await ctx.channel.send(embed = jokenpo_erro())

    @commands.command()
    async def jokenpo(self, ctx, choice):
        choice = choice.lower()
        bot_choice = secrets.choice(['pedra', 'papel', 'tesoura'])

        if bot_choice == choice:
            await ctx.channel.send(embed = jokenpo_empate(bot_choice, ctx.author.name))

        elif ((bot_choice == 'pedra' and choice == 'tesoura') or (bot_choice == 'tesoura' and choice == 'papel') or (bot_choice == 'papel' and choice == 'pedra')):
            await ctx.channel.send(embed = jokenpo_bot(bot_choice, ctx.author.name))

        elif choice == 'pedra' or choice == 'papel' or choice == 'tesoura':
            await ctx.channel.send(embed = jokenpo_user(bot_choice, ctx.author.name))

        else:
            await ctx.channel.send(embed = jokenpo_erro())



def setup(client):
    client.add_cog(Jokenpo(client))
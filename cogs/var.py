import discord
from discord.ext import commands
from misc.embeds import criar_var, var_fail, var_final, var_autor, var_cancelado, var_erro
from settings.db_commands import mysql_command

class NewVar():

    def __init__(self, autor, motivo, ponto, alvo, voto):
        self.autor = autor
        self.motivo = motivo
        self.ponto = ponto
        self.alvo = alvo
        self.voto = voto
        NewVar.voto = voto

    @staticmethod
    async def add_voto(user, voto):

        if voto == '\u2705':
            NewVar.voto['votos'].append({'user': user, 'voto': '\u2705'})
            NewVar.voto['votop'] += 1

            await Var.msg.edit(embed = criar_var(Var.votacao))
            
        elif voto == '\u274c':
            NewVar.voto['votos'].append({'user': user, 'voto': '\u274c'})
            NewVar.voto['voton'] += 1

            await Var.msg.edit(embed = criar_var(Var.votacao))

    @staticmethod
    async def retira_voto(user, voto):

        cont = 0
        for name in NewVar.voto['votos']:
            if name['user'] == user and voto == name['voto']:

                NewVar.voto['votos'].pop(cont)

                if voto == '\u2705':
                    NewVar.voto['votop'] -= 1
                elif voto == '\u274c':
                    NewVar.voto['voton'] -= 1

                await Var.msg.edit(embed = criar_var(Var.votacao))

            cont += 1

class Var(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def var(self, ctx, ponto, nome, *, msg):

        try:
            nome = nome.lower().capitalize()
            assert self.msg_bot != None
            await ctx.channel.send(embed = var_fail())
            return

        except Exception:
            Var.votacao = NewVar(ctx.author.name, msg, ponto, nome, {"votos":[],"votop": 0,"voton": 0})
            self.votacao = Var.votacao
            self.ponto = int(ponto)

        self.data = mysql_command(f"select * from pnts", True)

        verif = False
        for i in range(len(self.data)):
           if self.data[i]['nome'] == nome:
               self.id = self.data[i]['id_pontos']
               self.ponto_atual = self.data[i]['pontos']
               verif = True
               break

        if not verif:
            return  
       
        self.msg_bot = await ctx.channel.send(embed = criar_var(self.votacao))
        Var.msg = self.msg_bot
        await self.msg_bot.add_reaction('✅')
        await self.msg_bot.add_reaction('❌')

    @commands.command()
    async def cancelarvar(self, ctx):

        try:
            assert ctx.author.name == self.votacao.autor

            self.msg_bot = None
            self.votacao = None
            await ctx.channel.send(embed = var_cancelado())

        except NameError:
            await ctx.channel.send(embed = var_erro())

        except AssertionError:
            await ctx.channel.send(embed = var_autor())

    async def verifica(self, voto):

        if voto['votop'] >= 5 or voto['voton'] >= 5:

            await self.msg_bot.delete()
        
            if voto['votop'] >= 5:
                resultado = 'Confirmado!'

                mysql_command(f"update pnts set pontos = {self.ponto + self.ponto_atual} where id_pontos = {self.id}")

            elif voto['voton'] >= 5:
                resultado = 'Anulado!'

            await self.msg_bot.channel.send(embed = var_final(self.votacao, resultado))
            self.votacao = None
            self.msg_bot = None 

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        try:
            assert user.name != self.msg_bot.author.name
            assert self.msg_bot != None
        except:
            return

        for name in NewVar.voto['votos']:
            if name['user'] == user.name:
                return

        await NewVar.add_voto(user.name, reaction.emoji)
        await Var.verifica(self, NewVar.voto)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        try:
            assert self.msg_bot != None
        except:
            return

        for name in NewVar.voto['votos']:
            if name['user'] == user.name and name['voto'] == reaction.emoji:
                
                await NewVar.retira_voto(user.name, reaction.emoji)
                await Var.verifica(self, NewVar.voto)

def setup(client):
    client.add_cog(Var(client))
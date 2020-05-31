import yaml, requests, discord
from settings.db_commands import mysql_command
from comandos.commandManager import manager
from datetime import datetime, timedelta

from comandos.moderacao.banwords import banWords
from comandos.moderacao.flood import flood
from comandos.moderacao.link import link
from comandos.moderacao.spamcaps import spamcaps

class Handler():

    with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)
    token = data['TOKEN_JWT']
    
    @classmethod
    def getData(cls, ctx):
        payload = {
            "x-access-token": cls.token,
            "guildID": str(ctx.guild.id)
        }

        data = requests.post('http://localhost:3000/guild/get', json= payload).json()[0]
        return data

    @classmethod
    def adicionaAvisoMute(cls, guild, user, tempo, table):
        intervalo = 0
        if tempo // 3600:
            tempo //= 3600
            intervalo = 'hour'

        elif tempo // 60 and not intervalo:
            tempo //= 60
            intervalo = 'minute'

        elif not intervalo:
            intervalo = 'second'

        mysql_command(f"insert into {table} (server, user, expires) value ({guild}, {user}, now() + interval {tempo} {intervalo})")

    @classmethod
    def verificaAviso(cls, guild, user, numMute, numKick, numBan):
        data = list(mysql_command(f"select * from aviso where server = {guild} and user = {user}", True))

        removed = False
        for aviso in data:
            if aviso['expires'] < datetime.today():
                mysql_command(f"delete from aviso where id = {aviso['id']}")
                removed = True

        if removed:
            data = list(mysql_command(f"select * from aviso where server = {guild} and user = {user}", True))

        if len(data) >= numMute and len(data) < numKick:
            return 'mute'

        elif len(data) >= numKick and len(data) < numBan:
            return 'kick'

        elif len(data) >= numBan:
            return 'ban'
        
        return 0

    @classmethod
    def verificaMute(cls, guild, user):
        mute = mysql_command(f"select * from mute where user = {user} and server = {guild}", True)

        if len(mute) != 0:
            mute = mute[0]

            if mute['expires'] < datetime.today():
                mysql_command(f"delete from mute where id = {mute['id']}")
                return False

            else:
                return mute['expires']

        else:
            return False

    @classmethod
    async def filter(cls, ctx, client):
        
        if ctx.author.bot:
            return
        
        # verifica se está mutado
        mute = cls.verificaMute(ctx.guild.id, ctx.author.id)
        if mute:
            await ctx.delete()
            await ctx.author.send(embed = discord.Embed(
                title = f'Você está mutado no {ctx.guild.name} por mais {str(mute - datetime.today()).split(".")[0]}',
                color = 0xff0000
            ))
            return

        data = cls.getData(ctx)

        # verifica se é um comando com o prefixo certo
        if ctx.content.lower().startswith(f'{data["prefix"]}'):
            msg = ctx.content.split(' ')
            comando = msg[0].split(f'{data["prefix"]}')

            # comando no chat proibido
            for chats in data['chatsDisable']:
                if chats == str(ctx.channel.id):
                    if data['chatsDisableMsg']:
                        await ctx.delete()
                        await ctx.author.send(embed = discord.Embed(
                            title = f'Não é permitido usar comandos no canal {ctx.channel.name} do servidor {ctx.guild.name}!',
                            color = 0xff0000
                        ))
                        return
                    else:
                        await ctx.channel.send(embed = discord.Embed(
                            title = 'Não é permitido usar comandos nesse canal!',
                            color = 0xff0000
                        ))
                        return

            # comando proibido
            for comands in data['comandos']:
                if comands == comando[1]:
                    return
            
            await manager(ctx, comando[1], msg, client)

        else:

            try:
                adm_roles = mysql_command(f"select id_role from adm_roles where server = {ctx.guild.id}", True)[0]['id_role']
            except Exception:
                adm_roles = 0

            for role in ctx.author.roles:
                if role.id == adm_roles:
                    return
            
            deletar = False

            if data['banWords']:
                word = banWords(ctx, data['banWordsList'])
                if word:
                    deletar = True
                    await ctx.author.send(embed = discord.Embed(
                        title = f'BannedWord: {word}',
                        color = 0xff0000
                    ))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')
            
            if data['flood']:
                word = flood(ctx)
                if word:
                    deletar = True
                    await ctx.author.send(embed = discord.Embed(
                        title = f'Flood: {word}',
                        color = 0xff0000
                    ))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')

            if data['link']:
                urls = link(ctx, data['linkList'])
                if urls:
                    deletar = True
                    await ctx.author.send(embed = discord.Embed(
                        title = f"Links Banidos: {urls}",
                        color = 0xff0000
                    ))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')
         
            if data['spamcaps']:
                spam = spamcaps(ctx)
                if spam:
                    deletar = True
                    await ctx.author.send(embed = discord.Embed(
                        title = 'SpamCaps',
                        color = 0xff0000
                    ))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')

            if deletar:
                await ctx.delete()      

        result = cls.verificaAviso(ctx.guild.id, ctx.author.id, data['numMute'], data['numKick'], data['numBan'])

        if result:
            if result == 'mute':
                cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoMute'], 'mute')
                await ctx.author.send(embed = discord.Embed(
                    title = f"Você foi mutado por {(datetime.today() + timedelta(seconds = data['tempoMute'])) - datetime.today()}",
                    color = 0xff0000
                ))
            elif result == 'kick':
                await ctx.guild.kick(ctx.author, reason= 'Teste Kick')
            elif result == 'ban':
                await ctx.guild.ban(ctx.author, reason= 'Teste Ban', delete_message_days= 7)
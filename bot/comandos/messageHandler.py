import yaml, requests, discord
from settings.db_commands import mysql_command
from comandos.commandManager import manager
from datetime import datetime, timedelta
from contextlib import suppress

from misc.embeds_moderation import comandos_error_dm, comandos_error_channel, embed_banWord, embed_flood, embed_link, embed_spamcaps, embed_mute, tempo_mute, dm_kick, dm_ban, dm_softban, mute_perma

from comandos.moderacao.banwords import banWords
from comandos.moderacao.flood import flood
from comandos.moderacao.link import link
from comandos.moderacao.spamcaps import spamcaps

class Handler():

    with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)
    uri = data['URI_API']
    token = data['TOKEN_JWT']
    
    @classmethod
    def getData(cls, ctx):
        payload = {
            "x-access-token": cls.token,
            "guildID": str(ctx.guild.id)
        }

        data = requests.post(f'{cls.uri}/guild/get', json= payload).json()[0]
        return data

    @classmethod
    def adicionaAvisoMute(cls, guild, user, tempo, table):

        if tempo == 0:
            mysql_command(f"insert into {table} (server, user, expires) value ({guild}, {user}, 0)")
            return

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
    def verificaAviso(cls, guild, user):
        data = list(mysql_command(f"select * from aviso where server = {guild} and user = {user}", True))

        removed = False
        for aviso in data:
            if aviso['expires'] < datetime.today():
                mysql_command(f"delete from aviso where id = {aviso['id']}")
                removed = True

        if removed:
            data = list(mysql_command(f"select * from aviso where server = {guild} and user = {user}", True))

        return len(data)

    @classmethod
    def verificaMute(cls, guild, user):
        mute = mysql_command(f"select * from mute where user = {user} and server = {guild}", True)

        if len(mute) != 0:
            mute = mute[0]

            if mute['expires'] == None:
                return None

            if mute['expires'] < datetime.today():
                mysql_command(f"delete from mute where id = {mute['id']}")
                return False
            else:
                return mute['expires']
        else:
            return False

    @classmethod
    async def filter(cls, ctx, client):
        
        # Verifica se a mensagem não é de BOT
        if ctx.author.bot:
            return
        
        # Verifica se está mutado
        mute = cls.verificaMute(ctx.guild.id, ctx.author.id)
        if mute:
            await ctx.delete()
            await ctx.author.send(embed= tempo_mute(ctx.guild.name, mute))
            return

        elif mute == None:
            await ctx.delete()
            await ctx.author.send(embed= mute_perma(ctx.guild.name))
            return

        data = cls.getData(ctx)

        # Verifica se é um comando com o prefixo certo
        if ctx.content.lower().startswith(f'{data["prefix"]}'):
            msg = ctx.content.split(' ')
            comando = msg[0].split(f'{data["prefix"]}')

            # Comando no chat proibido
            for chats in data['chatsDisable']:
                if chats == str(ctx.channel.id):
                    if data['chatsDisableMsg']:
                        await ctx.delete()
                        await ctx.author.send(embed= comandos_error_dm(ctx.channel.name, ctx.guild.name))
                        return
                    else:
                        await ctx.channel.send(embed= comandos_error_channel())
                        return

            # Comando proibido
            for comands in data['comandos']:
                if comands == comando[1]:
                    return
            
            await manager(ctx, comando[1], msg, client)

        else:

            # Verifica se não é adm
            try:
                adm_roles = mysql_command(f"select id_role from adm_roles where server = {ctx.guild.id}", True)[0]['id_role']
            except Exception:
                adm_roles = 0

            for role in ctx.author.roles:
                if role.id == adm_roles:
                    return

            # Auto Moderation            
            penalidade = False

            # Ban Words
            if data['banWords']:
                banWord = banWords(ctx, data['banWordsList'])
                if banWord:
                    penalidade = True
                    if data['localMsgAviso']:
                        msgBanWord = await ctx.author.send(embed= embed_banWord(banWord, ctx.author.name, ctx.guild.name))
                    else:
                        msgBanWord = await ctx.channel.send(embed= embed_banWord(banWord, ctx.author.name, ctx.guild.name))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')
            
            # Flood
            if data['flood']:
                floodword = flood(ctx)
                if floodword:
                    penalidade = True
                    if data['localMsgAviso']:
                        msgFlood = await ctx.author.send(embed= embed_flood(floodword, ctx.author.name, ctx.guild.name))
                    else:
                        msgFlood = await ctx.channel.send(embed= embed_flood(floodword, ctx.author.name, ctx.guild.name))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')

            # Link proibido
            if data['link']:
                urls = link(ctx, data['linkList'])
                if urls:
                    penalidade = True
                    if data['localMsgAviso']:
                        msgLink = await ctx.author.send(embed= embed_link(urls, ctx.author.name, ctx.guild.name))
                    else:
                        msgLink = await ctx.channel.send(embed= embed_link(urls, ctx.author.name, ctx.guild.name))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')
         
            # Spam de CAPS
            if data['spamcaps']:
                spam = spamcaps(ctx)
                if spam:
                    penalidade = True
                    if data['localMsgAviso']:
                        msgSpam = await ctx.author.send(embed= embed_spamcaps(ctx.author.name, ctx.guild.name))
                    else:
                        msgSpam = await ctx.channel.send(embed= embed_spamcaps(ctx.author.name, ctx.guild.name))
                    cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoAviso'], 'aviso')

            # Verifica se a mensagem vai ser deletada
            if penalidade:
                await ctx.delete()      

        numAvisos = cls.verificaAviso(ctx.guild.id, ctx.author.id)

        # Verifica penalidades
        if numAvisos != 0 and penalidade:

            # BAN
            if numAvisos >= data['numBan'] and data['numBan']:
                await ctx.author.send(embed= dm_ban(ctx.guild.name, data['numBan']))
                await ctx.guild.ban(ctx.author, reason= f'Ban: Atingiu um total de {data["numBan"]} avisos', delete_message_days= 7)

            # SOFTBAN
            if numAvisos >= data['numSoftBan'] and data['numSoftBan']:
                await ctx.author.send(embed= dm_softban(ctx.guild.name, data['numSoftBan']))                
                await ctx.guild.ban(ctx.author, reason= f'SoftBan: Atingiu um total de {data["numSoftBan"]} avisos', delete_message_days= 7)
                await ctx.guild.unban(ctx.author, reason= f'SoftBan: Atingiu um total de {data["numSoftBan"]} avisos')

            # KICK
            if numAvisos >= data['numKick'] and data['numKick']:
                await ctx.author.send(embed= dm_kick(ctx.guild.name, data['numKick']))
                await ctx.guild.kick(ctx.author, reason= f'Atingiu um total de {data["numKick"]} avisos')

            # MUTE
            if numAvisos >= data['numMute'] and data['numMute']:
                cls.adicionaAvisoMute(ctx.guild.id, ctx.author.id, data['tempoMute'], 'mute')
                await ctx.author.send(embed= embed_mute(ctx.guild.name, data['tempoMute']))
   
        # Adiciona o numero de avisos na mensagem da penalidade
        with suppress(Exception):
            await msgBanWord.edit(embed= embed_banWord(banWord, ctx.author.name, ctx.guild.name, numAvisos))
        with suppress(Exception):
            await msgFlood.edit(embed= embed_flood(floodword, ctx.author.name, ctx.guild.name, numAvisos))
        with suppress(Exception):
            await msgLink.edit(embed= embed_link(urls, ctx.author.name, ctx.guild.name, numAvisos))                  
        with suppress(Exception):
            await msgSpam.edit(embed= embed_spamcaps(ctx.author.name, ctx.guild.name, numAvisos))
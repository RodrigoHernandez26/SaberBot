import discord
from datetime import datetime, timedelta

def comandos_error_dm(channel, guild):
    return discord.Embed(
        title = f'Não é permitido usar comandos no canal `{channel}` do servidor **{guild}**!',
        color = 0xff0000
    )

def comandos_error_channel():
    return discord.Embed(
        title = 'Não é permitido usar comandos nesse canal!',
        color = 0xff0000
    )

def embed_banWord(word, user, guild, avisos = 0):
    embed = discord.Embed(
        title = f'{user} recebeu um aviso por usar a palavra `{word}` no servidor **{guild}**!',
        color = 0xff0000
    )

    if avisos != 0:
        embed.set_footer(text= f'Você tem {avisos} aviso(s) no servidor {guild}.')

    return embed

def embed_flood(word, user, guild, avisos = 0):
    embed = discord.Embed(
        title = f'{user} recebeu um aviso por floodar a palavra `{word}` no servidor **{guild}**!',
        color = 0xff0000
    )
    
    if avisos != 0:
        embed.set_footer(text= f'Você tem {avisos} aviso(s) no servidor {guild}.')

    return embed

def embed_link(urls, user, guild, avisos = 0):
    embed = discord.Embed(
        title = f'{user} recebeu um aviso por enviar o(s) link(s) `{urls}` no servidor **{guild}**!',
        color = 0xff0000
    )
    
    if avisos != 0:
        embed.set_footer(text= f'Você tem {avisos} aviso(s) no servidor {guild}.')

    return embed

def embed_spamcaps(user, guild, avisos = 0):
    embed = discord.Embed(
        title = f'{user} recebeu um aviso por spammar caps lock no servidor **{guild}**!',
        color = 0xff0000
    )
    
    if avisos != 0:
        embed.set_footer(text= f'Você tem {avisos} aviso(s) no servidor {guild}.')

    return embed

def embed_mute(guild, tempoMute):
    if tempoMute == 0:
        return discord.Embed(
        title = f"Você foi mutado no **{guild}** pra `SEMPRE`",
            color = 0xff0000 
        )

    else:
        return discord.Embed(
        title = f"Você foi mutado no **{guild}** por `{(datetime.today() + timedelta(seconds = tempoMute)) - datetime.today()}`",
            color = 0xff0000 
        )

def tempo_mute(guild, tempo):
    return discord.Embed(
        title = f'Você está mutado no **{guild}** por mais `{str(tempo - datetime.today()).split(".")[0]}`',
        color = 0xff0000
    )

def mute_perma(guild):
    return discord.Embed(
        title = f'Você está mutado no **{guild}** pra `SEMPRE`!',
        color = 0xff0000
    )

def dm_kick(guild, numKick):
    return discord.Embed(
        title = f'Você foi kickado do **{guild}** por atingir `{numKick}` avisos.',
        color = 0xff0000
    )

def dm_softban(guild, numSoftBan):
    return discord.Embed(
        title = f'Você tomou um SoftBan no **{guild}** por atingir `{numSoftBan} avisos.`',
        color = 0xff0000
    )

def dm_ban(guild, numBan, tempo = 0): #por enquanto todos são permanentes
    embed = discord.Embed(
        title = f'Você foi banido do **{guild}** por atingir `{numBan}` avisos.',
        color = 0xff0000
    )
    if not tempo:
        embed.set_footer(text= f'O seu ban é `PERMANENTE`.')
    else:
        embed.set_footer(text= f'O seu ban dura por mais `{str(tempo - datetime.today()).split(".")[0]}`.')
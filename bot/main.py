
import sys

def dependencias():
    from verifyDependencies import Verify

    print('Verificando dependencias...', end='')

    if Verify.requirements():
        if Verify.settingsFile():
            if Verify.validSettignsFile():
                return True
            else:
                print('\nError: Complete todos os valores em ./settings/settings.yaml')
                return False
        else:
            print('\nError: Não foi encontrado o arquivo settings.yaml\nCrie um igual ao ./settings/settings.yaml.example')
            return False
    else:
        print('\nError: Run requirements.txt in pip==20.0.2')
        return False 


if dependencias():
    print('OK\nCarregando comandos...', end='')
else:
    sys.exit()

import discord
import yaml
import requests
from datetime import datetime
from settings.db_commands import connect
from comandos.messageHandler import Handler
from comandos.rpg.dado import dado
from misc import autoRole

global client
client = discord.Client()
with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)

@client.event
async def on_guild_join(guild):
    # real payload
    # payload = {
    #     "x-access-token": data['TOKEN_JWT'],
    #     "guildID": str(guild.id)
    # }

    # testing payload
    payload = {
        "x-access-token": data['TOKEN_JWT'],
        "guildID": str(guild.id),
        "comandos": ['add'],
        "chatsDisable": ['678697096454471713'],
        "chatsDisableMsg": True,
        "numMute": 3,
        "numKick": 5,
        "numBan": 7,
        "banWords": True,
        "banWordsList": ['teste', 'teste2'],
        "flood": True,
        "link": True,
        "linkList": ['https://www.google.com.br', 'https://www.youtube.com'],
        "spamcaps": True,
        "nomeAutoRole": 'cargo',
        "tempoAutoRole": 5
    }
    
    requests.post('http://localhost:3000/guild/sign', json= payload)

@client.event
async def on_guild_remove(guild):
    payload = {
        "x-access-token": data['TOKEN_JWT'],
        "guildID": str(guild.id)
    }
    requests.delete('http://localhost:3000/guild/delete', json= payload)

@client.event
async def on_ready():
    print('OK')
    print(datetime.now().strftime('\n%d/%m/%Y - %H:%M:%S\n'))

    try:
        connect()
    except Exception as e:
        print(f'Erro!\n{e}')
        
    await client.change_presence(status=discord.Status.online, activity=discord.Game("?help para ajuda"))
    print('[*] Bot online')

@client.event
async def on_message(ctx):
    await dado(ctx)
    await Handler.filter(ctx, client)

@client.event
async def on_member_join(member):
    await autoRole.autoRole(member)

client.run(data['TOKEN_DISCORD'])
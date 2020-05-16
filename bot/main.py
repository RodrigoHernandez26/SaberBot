import sys
import json
import os

try:
    import discord
    import MySQLdb
    import requests
    import yaml
    from discord.ext import commands
    from discord.ext.commands import CommandNotFound

except Exception:
    print('Run requirements.txt in pip==20.0.2')
    sys.exit()

try:
    with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)

except Exception:
    print('Não foi encontrado o arquivo settings.yaml\nCrie um igual ao ./settings/settings.yaml.example')
    sys.exit()

try:
    assert data['TOKEN_DISCORD'] != None
    assert data['PREFIX'] != None
    assert data['LIM_ADD'] != None
    assert data['LIM_MULT'] != None
    assert data['LIM_QNT'] != None
    assert data['LIM_DADO'] != None
    assert data['TOKEN_JWT'] != None
    assert data['RNG_KEY'] != None
    assert data['RNG_ID'] != None
    assert data['HOST'] != None
    assert data['USER'] != None
    assert data['PASSWORD'] != None
    assert data['DB'] != None
    assert data['PORT'] != None

except Exception:
    print('Complete todos os valores em ./settings/settings.yaml')
    sys.exit()

client = commands.Bot(command_prefix= data['PREFIX'], help_command= None)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

@client.event
async def on_guild_join(guild):
    payload = {
        "x-access-token": data['TOKEN_JWT'],
        "guildID": guild.id
    }
    requests.post('http://127.0.0.1:3000/guild/sign', json= payload)

@client.event
async def on_guild_remove(guild):
    payload = {
        "x-access-token": data['TOKEN_JWT'],
        "guildID": guild.id
    }
    requests.delete('http://127.0.0.1:3000/guild/delete', json= payload)

try:
    assert len(os.listdir('./bot/cogs')) == 0
    print('Nenhum comando criado em ./cogs')
    sys.exit()

except Exception:
    cont = 1
    for filename in os.listdir('./bot/cogs'):
        if filename.endswith('.py'):

            try:
                client.load_extension(f'cogs.{filename[:-3]}')

            except Exception as erro:
                print(f'Problema ao carregar {filename}\n{erro}')
                sys.exit()
            
            print(f'{cont} - {filename[:-3]} loaded!')
            cont += 1        

try:
    client.run(data['TOKEN_DISCORD'])

except Exception as erro:
    print(f'Impossível conectar ao bot - {erro}')
    sys.exit()
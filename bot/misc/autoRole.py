import requests
import yaml
import asyncio
import discord

def getData(guild):

    with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)

    payload = {
        "x-access-token": data['TOKEN_JWT'],
        "guildID": str(guild)
    }

    data = requests.post(f'{data["URI_API"]}/guild/get', json= payload).json()[0]
    return data

async def autoRole(member):
    data = getData(member.guild.id)
    await asyncio.sleep(data['tempoAutoRole'])
    role = discord.utils.get(member.guild.roles, name= data['nomeAutoRole'])
    await member.add_roles(role)
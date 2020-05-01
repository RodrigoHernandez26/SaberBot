import discord
from discord.ext import commands
import requests
import yaml
import json

async def parser(ctx, mult, mod, sinal, resultado):

    splited = []
    len_r = len(resultado)

    for i in range(mult):
        start = int(i*len_r/mult)
        end = int((i+1)*len_r/mult)
        splited.append(resultado[start:end])

    msg_final = f'<@!{ctx.author.id}> - {ctx.content}:'
    for i in range(mult):
        soma = sum(splited[i])
        splited[i].sort(reverse = True)

        if sinal == '+':
            soma += mod
            msg_final += f'\n{soma} - {splited[i]} + {mod}'

        elif sinal == '-':
            soma -= mod
            msg_final += f'\n{soma} - {splited[i]} - {mod}'

        else:
            msg_final += f'\n{soma} - {splited[i]}'

    await ctx.channel.send(msg_final)

def api_request(qnt, dado):

    reqData = {
                "jsonrpc": "2.0",
                "method": "generateIntegers",
                "params": {
                    "apiKey": "00000000-0000-0000-0000-000000000000",
                    "n": 10,
                    "min": 1,
                    "max": 10,
                    "replacement": True,
                    "base": 10
                },
                "id": 13058
            }

    with open('settings/settings.yaml', 'r') as f: reqKey = yaml.load(f, Loader= yaml.FullLoader)

    reqData['params']['apiKey'] = reqKey['API_KEY']
    reqData['id'] = reqKey['API_ID']
    reqData['params']['n'] = str(qnt)
    reqData['params']['max'] = str(dado)

    response = requests.post('https://api.random.org/json-rpc/2/invoke', json = reqData)
    response.raise_for_status()
    json = response.json()
    data = json['result']['random']['data']

    # O Bot limita as requests quando atinge esses valores
    # Para desativar essa função é só apagar essas linhas do if abaixo ou o comando que escreve no arquivo settings.yaml
    if json['result']['bitsLeft'] <= 100 or json['result']['requestsLeft'] <= 10:
        reqKey['API_KEY'] = None
        with open('settings/settings.yaml', 'w') as f: yaml.dump(reqKey, f)

    return data

class Dado(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        
        try:
            ctx.content[0]
        except Exception:
            return

        conteudo = ctx.content

    # ****** Multiplicador ****** #
        conteudo = conteudo.split('#')
        mult = conteudo[0]

        if mult == ctx.content:
            conteudo = mult
            mult = 1

        else:
            try:
                int(mult)
            except ValueError:
                return
            conteudo = conteudo[1]

    # ****** Quantidade ****** #
        conteudo = conteudo.split('d')
        qnt = conteudo[0]
        if qnt == '':
            conteudo = conteudo[1]
            qnt = 1
        else:
            try:
                int(qnt)
            except ValueError:
                return
            conteudo = conteudo[1]

    # ****** Dado e Modificador ****** #
        if conteudo.split('-')[0] == conteudo:
            if conteudo.split('+')[0] == conteudo:
                dado = conteudo
                mod = 0
                sinal = None

            else:
                conteudo = conteudo.split('+')
                dado = conteudo[0]
                sinal = '+'
                mod = conteudo[1]

        else:
            conteudo = conteudo.split('-')
            dado = conteudo[0]
            sinal = '-'
            mod = conteudo[1]

        try:
            int(dado)
            int(mod)
        except ValueError:
            return

        with open('settings/settings.yaml', 'r') as f: settings = yaml.load(f, Loader= yaml.FullLoader)

        if int(mult) > settings['LIM_MULT'] or int(qnt) > settings['LIM_QNT'] or int(dado) > settings['LIM_DADO']:
            return

        resultado = api_request(int(qnt)*int(mult), int(dado))
        await parser(ctx, int(mult), int(mod), sinal, resultado)

def setup(client):
    client.add_cog(Dado(client))
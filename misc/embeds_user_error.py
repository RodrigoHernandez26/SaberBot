import discord

def jokenpo_erro():

    embed = discord.Embed(
        title = f'`?help` para ver todos os comandos',
        color = 0xff0000
    )
    embed.add_field(name= f'`?jokenpo`', value= f'**Jogar pedra, papel ou tesoura com o Bot!\n\nComo usar?**', inline= False)
    embed.add_field(name= f'**Exemplos:**', value= f'`?jokenpo pedra`\n`?jokenpo papel`\n`?jokenpo tesoura`', inline= False)

    return embed

def add_erro():
    embed = discord.Embed(
        title = f'`?help` para ver todos os comandos',
        color = 0xff0000
    )
    embed.add_field(name= f'`?add`', value= f'**Adiciona pontos a alguem no jogo.\n\nComo usar?**', inline= False)
    embed.add_field(name= f'**Exemplos:**', value= f'`?add` `pontos` `Nome`', inline= False)

    return embed

def retirar_erro():
    embed = discord.Embed(
        title = f'`?help` para ver todos os comandos',
        color = 0xff0000
    )
    embed.add_field(name= f'`?retirar`', value= f'**Retira pontos a alguem no jogo.\nVerifique se esse comando vai deixa-lo com pontos negativos\n\nComo usar?**', inline= False)
    embed.add_field(name= f'**Exemplos:**', value= f'`?retirar` `pontos` `Nome`', inline= False)

    return embed

def novo_erro():
    embed = discord.Embed(
        title = f'`?help` para ver todos os comandos',
        color = 0xff0000
    )
    embed.add_field(name= f'`?novo`', value= f'**Adiciona alguém ao jogo.\nVerifique se o nome já foi adicionado**', inline= False)
    embed.add_field(name= f'**Exemplos:**', value= f'`?novo` `Nome`', inline= False)

def erro(nome):
    embed = discord.Embed(
        title = f'O `{nome}` não está no jogo!',
        color = 0xff0000
    )
    embed.set_footer(text = '?help para ajuda')
    embed.add_field(name = '**Dica:**', value = 'Use o `?pontos` pra verificar o nome dos participantes.', inline = False)

    return embed
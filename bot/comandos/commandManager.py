import os
import sys

try:
    from comandos.pontos.add import add
    from comandos.pontos.novo import novo
    from comandos.pontos.pontos import pontos
    from comandos.pontos.remover import remover
    from comandos.pontos.reset import reset
    from comandos.pontos.retirar import retirar

    from comandos.misc.coinflip import coinflip
    from comandos.misc.help import help
    from comandos.misc.jokenpo import jokenpo
    from comandos.misc.ping import ping
    from comandos.misc.setadm import setadm

    print('OK\nConectando...',end='')

except Exception as e:
    print(f'Erro!\nErro ao carregar comandos!\n{e}')
    sys.exit()

global comandos
comandos = []

for files in os.listdir('bot/comandos/pontos'):
    if files.endswith('.py'):
        comandos.append(files[:-3])

for files in os.listdir('bot/comandos/misc'):
    if files.endswith('.py'):
        comandos.append(files[:-3])

async def manager(ctx, comando, msg, client):

    del msg[0]
    for i in range(len(comandos)):
        if comandos[i] == comando:
            await eval(comandos[i])(ctx, msg, client)
    
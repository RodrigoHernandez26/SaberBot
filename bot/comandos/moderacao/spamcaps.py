
def spamcaps(ctx):

    if len(ctx.content) == 0:
        return

    cont = 0
    for char in list(ctx.content):
        if char.isupper():
            cont += 1
    
    if (cont * 100) / len(list(ctx.content)) >= 70:
        return True
    return False
class SpamCaps():

    @staticmethod
    async def spamcaps(ctx):
        cont = 0
        for char in list(ctx.content):
            if char.isupper():
                cont += 1
        
        if (cont * 100) / len(list(ctx.content)) >= 70:
            await ctx.channel.send('SpamCaps')
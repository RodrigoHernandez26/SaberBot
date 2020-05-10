class Badword():

    @staticmethod
    def getBadWordsList():
        return ['teste2', 'teste3']

    @staticmethod
    async def verifyBadWords(ctx):
        for word in Badword.getBadWordsList():
            if word in ctx.content.split():
                await ctx.channel.send(f'BannedWord: {word}')
                break
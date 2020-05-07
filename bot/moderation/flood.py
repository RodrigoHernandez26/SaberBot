class Flood():

    @staticmethod
    async def flood(ctx):
        counts = {}
        for word in ctx.content.split():
            if word not in counts:
                counts[word] = 0
            counts[word] += 1

            if counts[word] >= 5:
                await ctx.channel.send(f'Flood: {word}')
                break
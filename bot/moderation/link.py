import re

class Link():

    @staticmethod
    async def link(ctx):
        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', ctx.content)
        for url in urls:
            await ctx.channel.send(f'Link proibido: {url}')
        
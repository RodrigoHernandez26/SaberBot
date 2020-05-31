import re

def link(ctx, lista):
    urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', ctx.content)
    for url in urls:
        if url in lista:
            urls.remove(url)
    if len(urls) != 0:
        return urls
    else:
        return False
        
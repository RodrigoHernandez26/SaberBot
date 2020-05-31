
def banWords(ctx, data):

    for word in data:
        if word in ctx.content.split():
            return word
    return False
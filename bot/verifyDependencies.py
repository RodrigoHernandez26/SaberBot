
class Verify():

    @staticmethod
    def requirements():

        try:
            import discord
            import MySQLdb
            import requests
            import yaml
            from discord.ext import commands
            from discord.ext.commands import CommandNotFound
            return True

        except Exception:
            return False

    @staticmethod
    def settingsFile():
        
        import yaml

        try:
            with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)
            return True

        except Exception:
            return False

    @staticmethod
    def validSettignsFile():

        import yaml
        with open('./bot/settings/settings.yaml', 'r') as f: data = yaml.load(f, Loader= yaml.FullLoader)

        try:
            assert data['TOKEN_DISCORD'] != None
            assert data['PREFIX'] != None
            assert data['LIM_ADD'] != None
            assert data['LIM_MULT'] != None
            assert data['LIM_QNT'] != None
            assert data['LIM_DADO'] != None
            assert data['TOKEN_JWT'] != None
            assert data['RNG_KEY'] != None
            assert data['RNG_ID'] != None
            assert data['HOST'] != None
            assert data['USER'] != None
            assert data['PASSWORD'] != None
            assert data['DB'] != None
            assert data['PORT'] != None
            return True

        except Exception:
            return False
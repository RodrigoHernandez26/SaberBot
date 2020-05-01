import MySQLdb
import yaml

def connect():

    with open('settings/settings.yaml', 'r') as f: settings = yaml.load(f, Loader= yaml.FullLoader)

    global connection
    connection = MySQLdb.connect(settings['HOST'], settings['USER'], settings['PASSWORD'], settings['DB'], settings['PORT'])
    print('[*] Bot conectado ao db: ' + settings['DB'])

    global c
    c = connection.cursor(MySQLdb.cursors.DictCursor)

def mysql_command(query, fet = False):
    c.execute(query)
    connection.commit()
    
    if fet:
        return c.fetchall()
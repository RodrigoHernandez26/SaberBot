from flask import Flask, request, redirect, session, render_template, url_for, make_response, session
from oauth2 import OAuth
from settings.db_commands import connect, mysql_command
import requests
from datetime import timedelta

connect()

app = Flask(__name__)
app.secret_key = 'SXSrHviCf2VqUVAv0EJB8w'
app.permanent_session_lifetime = timedelta(hours=2)

BotName = "SaberBot"

@app.route('/')
def index():
    return render_template('index.html', BotName= BotName)

@app.route('/invite/')
def invite():
    return redirect('https://discordapp.com/oauth2/authorize?client_id=705878925363904543&scope=bot&permissions=8')

@app.route('/status/')
def status():
    try:
        db = True
        data = mysql_command('select rand, disc from status_api where id = 1', True)
    except Exception:
        db = False
    return render_template('status.html', random= data[0]['rand'], discord= data[0]['disc'], db = db, BotName = BotName)

@app.route('/login/')
def login():

    if session.get('TOKEN', None) is not None:
        return redirect('/dashboard/home/')
    else:
        return redirect(OAuth.discord_login_url)

@app.route('/dashboard/')
def dashboard():

    try:
        code = request.args.get('code')
        assert code != None
    except:
        return redirect('/')

    access_token = OAuth.get_access_token(code)
    user_info = OAuth.get_user_info(access_token)
    user_guilds = OAuth.get_user_guilds(access_token)
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_info["id"]}/{user_info["avatar"]}.png?size=256'

    adm_guilds = []
    for guilds in user_guilds:
        if guilds['permissions'] == 2147483647 or guilds['owner']:
            adm_guilds.append(guilds)
     
    payload = {
        "user_info": user_info,
        "user_guilds": adm_guilds,
        "avatar_url": avatar_url
    }

    token = requests.post('http://127.0.0.1:3000/token/', json= payload).json()['token']

    session.permanent = True
    session['TOKEN'] = token

    return redirect(url_for("dashHome"))

@app.route("/dashboard/home/")
def dashHome():

    if session.get('TOKEN', None) is not None:
        token = session.get('TOKEN')
    else:
        return redirect(url_for('index'))

    try:
        payload = {
            "x-access-token": token
        }

        data = requests.post('http://127.0.0.1:3000/data/', json= payload)
        assert data.status_code != 401
        data = data.json()['data']

    except:
        return redirect(OAuth.discord_login_url)

    user_info = data['user_info']
    user_guilds = data['user_guilds']
    avatar_url = data['avatar_url']

    return render_template('dashboard.html', user_info= user_info, user_guilds= user_guilds, avatar_url = avatar_url, BotName = BotName)

@app.route('/dashboard/guild/', defaults= {'guild_id': "0"})
@app.route('/dashboard/guild/<guild_id>/<guild_name>')
def guild(guild_id, guild_name):
    if guild_id == '0':
        return redirect('/index/')

    if session.get('TOKEN', None) is not None:
        token = session.get('TOKEN')
    else:
        return redirect(url_for('index'))

    try:
        payload = {
            'x-access-token': token,
            "guildID": guild_id
        }

        data = requests.post('http://localhost:3000/guild/get', json= payload).json()[0]

    except IndexError: 
        return redirect('https://discordapp.com/oauth2/authorize?client_id=705878925363904543&scope=bot&permissions=8')

    except Exception:
        return redirect('/login/')

    return render_template('guild.html', BotName= BotName, guild_name= guild_name, data= data)

@app.route("/logout/")
def logout():
	session['TOKEN'] = None
	return redirect(url_for("index"))

if (__name__ == "__main__"):
    #app.run(host= '0.0.0.0', port= 80) #gcp
    app.run(debug= True) #dev
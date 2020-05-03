from flask import Flask, request, redirect, session, render_template, url_for, make_response
from oauth2 import OAuth
from settings.db_commands import connect, mysql_command
import requests

connect()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    return redirect(OAuth.discord_login_url)

@app.route('/invite/')
def invite():
    return redirect('https://discordapp.com/oauth2/authorize?client_id=705878925363904543&scope=bot&permissions=2048')

@app.route('/dashboard/guild/', defaults= {'guild_id': "0"})
@app.route('/dashboard/guild/<guild_id>')
def guild(guild_id):
    if guild_id == '0':
        return redirect('/login/')
    return render_template('guild.html')

@app.route('/dashboard/guild/<guild_id>/config')
def config(guild_id):
    return render_template('config.html')

@app.route('/status/')
def status():
    try:
        db = True
        data = mysql_command('select rand, disc from status_api where id = 1', True)
    except Exception:
        db = False
    return render_template('status.html', random= data[0]['rand'], discord= data[0]['disc'], db = db)

@app.route('/dashboard/')
def dashboard():
    code = request.args.get('code')
    access_token = OAuth.get_access_token(code)

    # token = requests.post('http://127.0.0.1:3000/token/', json= {"access_token": access_token}).json()['token']

    global user_info
    user_info = OAuth.get_user_info(access_token)
    global user_guilds
    user_guilds = OAuth.get_user_guilds(access_token)
    global avatar_url
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_info["id"]}/{user_info["avatar"]}.png?size=256'
    return dashHome()

@app.route('/dashboard/home/')
def dashHome():
    return render_template('dashboard.html', user_info= user_info, user_guilds= user_guilds, avatar_url = avatar_url)

if (__name__ == "__main__"):
    app.run(debug=True)
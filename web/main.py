from flask import Flask, request, redirect, session, render_template, url_for
from oauth2 import OAuth

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(OAuth.discord_login_url)

@app.route('/invite')
def invite():
    return redirect('https://discordapp.com/oauth2/authorize?client_id=679153754175701032&scope=bot&permissions=2048')

@app.route('/dashboard')
def dashboard():
    code = request.args.get('code')
    access_token = OAuth.get_access_token(code)
    user_info = OAuth.get_user_info(access_token)
    user_guilds = OAuth.get_user_guilds(access_token)
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_info["id"]}/{user_info["avatar"]}.png?size=40'
    return render_template('dashboard.html', user_info= user_info, user_guilds= user_guilds, avatar_url = avatar_url)

if (__name__ == "__main__"):
    app.run(debug=True)
from os import environ, urandom
import json
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)

app.secret_key = urandom(24)

names = []
user = []
users = []
game_over = False

@app.route('/')
def index():
    with open("data/data.json", "r") as json_data:
        session['data'] = json.load(json_data)
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
    
@app.route('/logout')
def logout():
    for n in user:
        if n['name'] == session['user']:
          user.remove(n)
    user.append({"name": session['user'], "score": session['score']})
    session.pop('user', None)
    return render_template(
        'leaderboard.html',
        title='Leaderboard',
        year=datetime.now().year,
        scores = user
    )
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(session['user'])
    if request.method == "POST":
        if request.form["name"] in names:
            message = "The user name " + request.form["name"] + " is taken, try another username"
            flash(message)
            return render_template('login.html', title='Home Page', year=datetime.now().year)
        else:
            names.append(request.form["name"])
            session['user'] = request.form["name"]
            session['score'] = 0
            session['question'] = 0
        return redirect(session['user'])
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
    )

@app.route('/<name>', methods=["GET", "POST"])
def game(name):
    if name == "favicon.ico":
        return redirect('/')
    session['total'] = 5
    session['question'] = 0
    global question
    if request.method == "POST" and request.form["answer"] == session['data'][session['question']]['answer']:
        session['score'] += 1
        session['question'] += 1
        session['total'] -= 1
        return redirect('/' + name)
    if request.method == "POST" and request.form["answer"] != session['data'][session['question']]['answer']:
        message = "Answer " + request.form["answer"] + " is incorrect, please try again."
        flash(message)
        return redirect('/' + name)
    return render_template("game.html", page_title = "Java Quiz", data = session['data'][session['question']], year=datetime.now().year)


if environ.get('DEVELOPMENT'):
    development = True
else:
    development = False

if __name__ == '__main__':
    HOST = environ.get('IP')
    if development:
        PORT = int(environ.get('C9_PORT'))
    else:
        PORT = int(environ.get('PORT'))
    app.run(HOST, PORT, debug=development)
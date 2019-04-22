from flask import Flask, request, session, render_template, redirect, url_for
from flask_basicauth import BasicAuth
import json
from flask import jsonify
import datetime

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days= 365)
app.secret_key = 'asdsaffgsdgf'

app.config['BASIC_AUTH_USERNAME'] = 'TRAIN'
app.config['BASIC_AUTH_PASSWORD'] = 'TuN3L'
id = 1
basic_auth = BasicAuth(app)


@app.route('/')
def hi():
    return 'HI!'


@app.route('/login', methods=['POST', 'GET'])
@basic_auth.required
def login():
    if basic_auth.authenticate() is True:
        session['username'] = session.get('username', 'TRAIN')
        return redirect(url_for('hello'))
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('hi'))
    else:
        return redirect(url_for('login'))


@app.route('/hello')
def hello():
    if 'username' in session:
        return render_template('greeting.html', user=session['username'])
    else:
        return redirect(url_for('login'), code=401)


@app.route('/trains', methods=['GET', 'POST'])
def trains():
    if 'username' not in session:
        return redirect(url_for('login'), code=401)

    global id
    if request.method == 'POST':
        js = request.get_json()
        id += 1
        f = open('database.json', 'r')
        datastore = json.load(f)
        f.close()
        f = open('database.json', 'w')
        datastore[f'uuid{id - 1}'] = js
        json.dump(datastore, f)
        f.close()
        return redirect(url_for('trains_id', id=f'uuid{id - 1}'))
    else:
        f = open('database.json', 'r')
        datastore = json.load(f)
        f.close()
        return jsonify(datastore)


@app.route('/trains/<id>', methods=['GET', 'DELETE'])
def trains_id(id):
    if 'username' not in session:
        return redirect(url_for('login'), code=401)

    if request.method == 'GET':
        if 'username' not in session:
            return redirect(url_for('login'), code=401)
        f = open('database.json', 'r')
        datastore = json.load(f)
        f.close()
        return jsonify(datastore[id])

    elif request.method == "DELETE":
        f = open('database.json', 'r')
        datastore = json.load(f)
        f.close()
        if id in datastore:
            del datastore[id]
            f = open('database.json', 'w')
            json.dump(datastore, f)
            f.close()
        return '', 204


if __name__ == "__main__":
    app.run(debug=True)

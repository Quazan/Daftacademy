from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

counter = 0


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/request')
def request_info():
    return f'request method: {request.method} url: {request.url} headers: {request.headers}'


@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_method():
    return request.method


@app.route('/show_data', methods=['POST'])
def show():
    #return request.data
    return jsonify(request.json)


@app.route('/pretty_print_name', methods=['POST'])
def print_name():
    content = request.get_json(silent=True)
    name = content['name']
    surename = content['surename']
    return f'Na imię mu {name}, a nazwisko jego {surename}'


@app.route('/counter')
def count():
    global counter
    counter += 1
    return f'{counter}'


if __name__ == '__main__':
    app.run(debug=True)

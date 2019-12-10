from flask import Flask, render_template, request
from forms import LoginForm

app = Flask(__name__)


@app.route('/')
def index():
    user = {'username': 'Молодой человек'}
    return render_template('index.html', title='Web', user=user)


@app.route('/login/', methods=['post', 'get'])
def login():
    # message = ''
    # if request.method == 'POST':
    #    username = request.form.get('username')
    #    password = request.form.get('password')

    # if username == 'root' and password == 'pass':
    #    message = "Correct username and password"
    # else:
    #    message = "Wrong username or password"

    return render_template('login.html')


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
from forms import LoginForm
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def index():
    user = {'username': 'Молодой человек'}
    return render_template('index.html', title='Web', user=user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userDetails = request.form
        email = userDetails['name']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email, password) VALUES(%s, %s)", (email,password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('login.html')


if __name__ == '__main__':  # запуск сервера
    app.run(debug=True)

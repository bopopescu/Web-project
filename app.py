from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL, MySQLdb
import yaml

app = Flask(__name__)

# database has name "data"
# table with email and password has name "users"
# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']

mysql = MySQL(app)


@app.route('/')
def index():
    user = {'username': 'Молодой человек'}
    return render_template('index.html', title='Web', user=user)


@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        user_details = request.form
        email = user_details['email']
        password = user_details['password']
        user_name = user_details['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email, password, user_name) VALUES(%s, %s, %s)", (email, password, user_name))
        mysql.connection.commit()
        # print(user_details)
        session['email'] = user_details['email']
        cur.close()
        return 'success'
    return render_template('sign-up.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # error_message = 'Incorrect login or password'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        curs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = curs.fetchone()
       # print("в переменной user хранится : ", user)
        curs.close()

        try:
            if len(user) > 0:
                if password == user['password']:
                    print(user)
                    return render_template('user.html', title='Home', user_name=user['user_name'])
                else:
                    return "Error: password and email don't match"
        except BaseException:
            return render_template('login.html')  # Здесь почему-то не выводится сообщение об ошибке :(

    return render_template('login.html')


if __name__ == '__main__':  # запуск сервера
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
#
app.secret_key = "12345678"


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
#    flash("I LOVE YOU")
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        phone = userDetails['phone']
        password = userDetails['password']
        confirm_password = userDetails['confirm_password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where phone_no='"+phone+"'")
        data = cur.fetchone()
        if data is not None:
            flash("Phone already registered")
            return redirect('/signup')
        else:
            cur.execute("SELECT * FROM users where email='"+email+"'")
            data = cur.fetchone()
            if data is not None:
                flash("Email already registered")
                return redirect('/signup')
            elif password==confirm_password:
                cur.execute("INSERT INTO users(name, email, phone_no, password) VALUES(%s, %s, %s, %s)",(name, email, phone, password))
                mysql.connection.commit()
                cur.close()
                flash("Registration Successful")
                return redirect('/login', "success")
            else:
                flash("Passwords doesnt match")
                return redirect('/signup')
            cur.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        email1 = userDetails['email']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email LIKE '"+email1+"' AND password LIKE '"+password+"'")
        data = cur.fetchone()
        if data is None:
            flash("Email or password is incorrect")
            return redirect('/login', "danger")
        else:
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

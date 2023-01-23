import crypt
import os
import cryptography
from flask import Flask, make_response, redirect, render_template, request, session, url_for
import psycopg2


app = Flask(__name__)



@app.route('/')
def index():
    template = render_template('index.html')
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = session.get('message', None)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid email or password.'
            return render_template('login.html', message=message)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        hashed_password = crypt.hashpw(password.encode('utf-8'), cryptography.gensalt())

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (fname, lname, email, password) VALUES (%s, %s, %s, %s)", (fname, lname, email, hashed_password))
        conn.commit()
        cur.close()
        session['message'] = 'Account created successfully.'
        return redirect(url_for('/login'))
    return render_template('register.html')





if __name__ == '__main__':
    app.run(debug=True)

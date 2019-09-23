from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, logging, send_from_directory
import os
app = Flask(__name__)
import random
from random import shuffle
import sqlite3
import time
import datetime
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from db_user import create_user, RegisterForm, retrieve_user_by_number,retrieve_user_by_username
from functools import wraps


@app.route("/login")
def trueme():
    redirecturl = "http://127.0.0.1:5001/"
    return render_template('trueme_login.html', redirecturl = redirecturl, client = "BrusselsAirlines")


# @app.route("/login", methods=['GET'])
# def f():
#     error = None
#     return render_template('trueme_login.html', error=error)

@app.route("/login", methods=['POST'])
def login():
    phonenumber = request.form['number']
    pw = request.form['password']
    user_row = retrieve_user_by_number(phonenumber)
    user = dict(user_row)
    if not sha256_crypt.verify(pw, user['PASSWORD']):
        message = f"Invalid Credentials. Please try again"
        return render_template('trueme_login.html', error=message)
    user_name = user['NAME']
    return redirect(f'http://127.0.0.1:5000/ask_game?user={user_name}')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        number = form.number.data
        id = random.randint(0,10000)
        password = sha256_crypt.encrypt(str(form.password.data))
        name = form.name.data
        surname= form.surname.data
        email= form.email.data
        create_user(id, number, password, name, surname, email)
        return redirect(f'/login')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=5001, debug=True)

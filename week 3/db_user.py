import sqlite3
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, logging, send_from_directory
import os
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import pdb

class RegisterForm(Form):
    number = StringField('number', [validators.Length(min=1, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')
    name = StringField('name', [validators.Length(min=1, max=50)])
    surname = StringField('surname', [validators.Length(min=1, max=50)])
    email = StringField('email', [validators.Length(min=1, max=50)])

def create_user(id, number, password, name, surname, email):
    conn = sqlite3.connect("trueme.sqlite")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query_string = '''
        INSERT INTO TRUEME (ID,NUMBER,PASSWORD,NAME,SURNAME,EMAIL)
        VALUES (?, ?, ?, ?, ?, ?);
    '''
    cursor.execute(query_string, (id, number, password, name, surname, email))
    conn.commit()
    conn.close()

def retrieve_user_by_number(phonenr):
	return query(f'SELECT * FROM TRUEME WHERE NUMBER = "{phonenr}"', one=True)

def retrieve_user_by_username(name):
    return query(f'SELECT NAME FROM TRUEME WHERE NAME = "{name}"', one=True)

def query(query_string, *args, one=False):
    con = sqlite3.connect("trueme.sqlite")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute(query_string, args)
    results = cursor.fetchall()
    cursor.close()
    return (results[0] if results else None) if one else results

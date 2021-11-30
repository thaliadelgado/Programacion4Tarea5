# Libraries
import app
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector as mariadb
import os
import json

# import pymysql

# Config JSON
with open('config.json', 'r') as file:
    config = json.load(file)

# DataBase connection config
mariadb = mariadb.connect(host=config['DB2']['DB_HOST'],
                          port=config['DB2']['DB_PORT'],
                          user=config['DB2']['DB_USER'],
                          passwd=config['DB2']['DB_PASS'],
                          db='dictionary')

# Work cursor
cursor = mariadb.cursor()

# set flask app
app = Flask(__name__)
app.secret_key = os.urandom(128)


# Routes
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.form.get('add') == 'add':
        word = request.form['word']
        definition = request.form['definition']
        insert = "INSERT INTO words (word, definition) VALUES ('" + word + "','" + definition + "')"
        cursor.execute(insert)
        mariadb.commit()
        flash('Palabra añadida con exito!!!')
        print('Presionaste el boton añadir')

    query = "SELECT * FROM words"
    cursor.execute(query)
    resp = cursor.fetchall()

    return render_template("index.html", data=resp)


@app.route("/delete/<id>")
def delete(id):
    delete = "DELETE FROM words WHERE Id_word = {}".format(id)
    cursor.execute(delete)
    mariadb.commit()
    flash('Palabra eliminada con exito!!!')
    return redirect(url_for('main_page'))


@app.route("/update/<id>", methods=['GET', 'POST'])
def update(id):

    if request.form.get('act') == 'act':
        definition = request.form['definition']
        update = "UPDATE words set definition = '{}' WHERE Id_word = '{}' ".format(definition,id)
        cursor.execute(update)
        mariadb.commit()
        flash('Palabra actualizada con exito!!!')
        return redirect(url_for('main_page'))

    query = "SELECT * FROM words WHERE Id_word = '{}'".format(id)
    cursor.execute(query)
    resp = cursor.fetchall()

    return render_template("update.html", data=resp)


if __name__ == '__main__':
    app.run(host='localhost', port='80', debug=True)

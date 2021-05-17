from wsgiref.simple_server import make_server
from flask import Flask, session, render_template, request, redirect, url_for

import mysql.connector as mysql
import os
import time
import datetime

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

app = Flask(__name__)

@app.route('/')
def get_home():
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Users;")
  records = cursor.fetchall()
  db.close()
  return render_template('home.html', users=records)


@app.route('/cv')
def cv():
  return render_template('home.html')


@app.route('/welcome')
def welcome():
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select id, name, email, comment from Users;")
  records = cursor.fetchall()
  db.close()
  print(records)
  return render_template('welcome.html', guestbook=records)


@app.route('/guestbook_form', methods=['POST'])
def guestbook():
  name = request.form['name']
  email = request.form['email']
  comment = request.form['message']

  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

  # query = (
  # "INSERT INTO users (name, email, comment, created_at) "
  # "VALUES (%s, %s, %s, %s)"
  # )
  # data = (name, email, comment, timestamp)

  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  
  query = "insert into Users (name, email, comment, created_at) values (%s, %s, %s, %s)"

  values = [
    (name, email, comment, timestamp)
  ]
  cursor.executemany(query, values)
  db.commit()
  db.close()
  return redirect(url_for('welcome'))

@app.route('/avatar')
def avatar():
  return {"image_src": "https://i.ibb.co/0nmJ0by/profile.jpg"}

@app.route('/personal')
def personal():
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Personal;")
  records = cursor.fetchall()
  db.close()
  return records

@app.route('/education')
def education():
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Education;")
  records = cursor.fetchall()
  db.close()
  return records

@app.route('/project')
def project():
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from Project;")
  records = cursor.fetchall()
  cursor.execute("select * from Team;")
  team = cursor.fetchall()
  db.close()
  return {**records, **team}

''' Route Configurations '''
if __name__ == '__main__':
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()
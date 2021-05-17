from wsgiref.simple_server import make_server
from flask import Flask, session, render_template, request, redirect, url_for

import mysql.connector as mysql
import os
import time
import datetime

AVATAR_LINK = "https://i.ibb.co/0nmJ0by/profile.jpg"

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

app = Flask(__name__)

def convert_json(record, rest):
  d = {}
  for i, field in enumerate(rest):
    d[field] = record[0][i]
  return d

def fetch_query(query):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(query)
  records = cursor.fetchall()
  db.close()
  return records

@app.route('/')
def get_home():
  records = fetch_query("select * from Users;")
  return render_template('home.html', users=records)


@app.route('/cv')
def cv():
  return render_template('home.html')


@app.route('/welcome')
def welcome():
  records = fetch_query("select id, name, email, comment from Users;")
  print(records)
  return render_template('welcome.html', guestbook=records)


@app.route('/guestbook_form', methods=['POST'])
def guestbook():
  name = request.form['name']
  email = request.form['email']
  comment = request.form['message']

  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

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
  return {"image_src": AVATAR_LINK}

@app.route('/personal')
def personal():
  records = fetch_query("select * from Personal;")
  print(records)
  return convert_json(records, ['first_name', 'last_name', 'email'])

@app.route('/education')
def education():
  records = fetch_query("select * from Education;")
  print(records)
  return convert_json(records, ['school', 'degree', 'major', 'date'])

@app.route('/project')
def project():
  records = fetch_query("select * from Project;")
  team = fetch_query("select * from Team;")
  print(records, team)
  teams = {f'api_link_{i}':url[0] for i, url in enumerate(team)}
  return {**convert_json(records, ['title', 'description', 'link', 'Image_src']), **{'team':teams}}

''' Route Configurations '''
if __name__ == '__main__':
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()
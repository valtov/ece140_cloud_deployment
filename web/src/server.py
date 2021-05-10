from wsgiref.simple_server import make_server
from flask import Flask, session, render_template, request

import mysql.connector as mysql
import os

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
  cursor.execute("select first_name, last_name, email from Users;")
  records = cursor.fetchall()
  db.close()

  return render_template('home.html', users=records)

''' Route Configurations '''
if __name__ == '__main__':

    server = make_server('0.0.0.0', 6000, app)
    server.serve_forever()
  # config = Configurator()

  # config.include('pyramid_jinja2')
  # config.add_jinja2_renderer('.html')

  # config.add_route('get_home', '/')
  # config.add_view(get_home, route_name='get_home')

  # config.add_static_view(name='/', path='./public', cache_max_age=3600)

  # app = config.make_wsgi_app()
  # server = make_server('0.0.0.0', 6000, app)
  # server.serve_forever()

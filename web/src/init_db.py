# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")

cursor.execute("drop table if exists Personal;")

cursor.execute("drop table if exists Education;")

cursor.execute("drop table if exists Project;")

cursor.execute("drop table if exists Team;")


def init_table(table, query, values):
  try:
    cursor.execute(table)
    cursor.executemany(query, values)
    db.commit()
  except:
    print("Table already exists. Not recreating it.")

table = """
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      comment     VARCHAR(150) NOT NULL,
      created_at  TIMESTAMP
    );
  """
query = "insert into Users (name, email, comment, created_at) values (%s, %s, %s, %s)"

values = [
  ('Rick Gessner', 'rick@gessner.com', 'I cant wait to come to the party!', '2021-05-18 12:00:00'),
  ('Ramsin Khoshabeh','ramsin@khoshabeh.com', 'Me too!', '2021-05-18 12:00:00')
]

init_table(table, query, values)

table = """
    CREATE TABLE Personal (
      first_name    VARCHAR(30) NOT NULL,
      last_name     VARCHAR(30) NOT NULL,
      email         VARCHAR(30) NOT NULL
    );
  """
query = "insert into Personal (first_name, last_name, email) values (%s, %s, %s)"

values = [
  ('Joe', 'Mama', 'valtov@ucsd.edu')
]

init_table(table, query, values)

table = """
    CREATE TABLE Education (
      school     VARCHAR(50) NOT NULL,
      degree     VARCHAR(50) NOT NULL,
      major      VARCHAR(50) NOT NULL,
      date       VARCHAR(50) NOT NULL
    );
  """
query = "insert into Education (school, degree, major, date) values (%s, %s, %s, %s)"

values = [
  ('UCSD', 'B.S', 'Computer Science', '2021')
]

init_table(table, query, values)

table = """
    CREATE TABLE Project (
      title           VARCHAR(150) NOT NULL,
      description     VARCHAR(150) NOT NULL,
      link            VARCHAR(150) NOT NULL,
      Image_src       VARCHAR(150) NOT NULL
    );
  """
query = "insert into Project (title, description, link, Image_src) values (%s, %s, %s, %s)"

values = [
  ('ServiceUP', 'Offerup but for services', 'link.com', 'img.com')
]

init_table(table, query, values)

table = """
    CREATE TABLE Team (
      api_link        VARCHAR(150) NOT NULL
    );
  """
query = "insert into Team (api_link) values (%s)"

values = [
  ('link1.com'),
  ('link2.com'), 
  ('link3.com')
]

init_table(table, query, values)

print('Got here')

# Selecting Records
cursor.execute("select * from Users;")
print('---------- Users INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Personal;")
print('---------- Personal INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Education;")
print('---------- Education INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Project;")
print('---------- Project INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from Team;")
print('---------- Team INITIALIZED ----------')
[print(x) for x in cursor]
db.close()
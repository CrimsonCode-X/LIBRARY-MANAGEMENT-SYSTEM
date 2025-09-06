import mysql.connector as conn

def get_db_connection():
  conn.connect( host = "localhost", user = "root", password = "root1234", database = "library_db")

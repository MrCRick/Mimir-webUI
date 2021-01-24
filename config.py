import os
import mysql.connector as mysql


SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
MYSQL_HOST=os.environ.get("MYSQL_HOST")
MYSQL_PSSW=os.environ.get("MYSQL_PASSWORD")
MYSQL_USER=os.environ.get("MYSQL_USER")
MYSQL_URL=os.environ.get("MYSQL_URL")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
APISERVER = os.environ.get("APISERVER")


basedir = os.path.abspath(os.path.dirname(__file__))



def createDB():
	db = mysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PSSW)
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS mimir")
	db.commit()
	db.close()


def createTables():
	db = mysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PSSW, database="mimir")
	cursor = db.cursor()
	cursor.execute("CREATE TABLE user ( id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(120), email VARCHAR(120), password_hash VARCHAR(120), enable BOOLEAN, is_admin BOOLEAN )")
	cursor.execute("CREATE TABLE user_object_id ( id INT AUTO_INCREMENT PRIMARY KEY, object_id INT, object_type VARCHAR(120), user_name VARCHAR(120))")
	db.commit()
	db.close()
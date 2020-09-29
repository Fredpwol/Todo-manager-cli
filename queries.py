import sqlite3
import sys

def create_db():
    db = sqlite3.connect(FILENAME)
    curr = db.cursor()
    curr.execute("CREATE TABLE users (id INT PRIMARY KEY , username VARCHAR(50) NOT NULL, password VARCHAR(16) NOT NULL)")
    curr.execute("CREATE TABLE task (id INT PRIMARY KEY, task VARCHAR(100) NOT NULL, status BOOLEAN DEFAULT 0 NOT NULL )")
    db.commit()
    curr.close()
    return db


def get_user(db, id):
    curr = db.cursor()
    user = curr.execute("SELECT username, password FROM users WHERE ID=?",(id,))
    db.commit()
    curr.close()
    
    return user.fetchone()



def create_user(db, username, password):
    curr = db.cursor()
    curr.execute("INSERT INTO users VALUES (NULL,?,?)",(username, password))
    curr.close()
    db.commit()

def list_users(db):
    curr = db.cursor()
    users = curr.execute("SELECT * from users")
    for user in users:
        sys.stdout.write(users)
    curr.close()

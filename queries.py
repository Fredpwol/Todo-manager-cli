import sqlite3
import uuid

FILENAME = "todo_cli.db"

def create_db():
    db = sqlite3.connect(FILENAME)
    curr = db.cursor()
    curr.execute("CREATE TABLE users (id VARCHAR(32), username VARCHAR(50) NOT NULL, password VARCHAR(16) NOT NULL)")
    curr.execute("CREATE TABLE task (id INTEGER PRIMARY KEY AUTOINCREMENT, task VARCHAR(100) NOT NULL, status BOOLEAN DEFAULT 0 NOT NULL )")
    db.commit()
    curr.close()
    return db


def get_user(db, username, password):
    curr = db.cursor()
    user = curr.execute("SELECT username, password FROM users WHERE username=? AND password=?",(username, password))
    db.commit()
    curr.close()
    
    return user.fetchone()



def create_user(db, username, password):
    curr = db.cursor()
    uid = uuid.uuid4().hex
    curr.execute("INSERT INTO users VALUES (?,?,?)",(uid,username, password))
    curr.close()
    db.commit()

def list_users(db):
    curr = db.cursor()
    users = curr.execute("SELECT username from users")
    for user in users:
        print(user[0])
    curr.close()

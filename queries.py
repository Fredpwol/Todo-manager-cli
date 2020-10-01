import sqlite3
import uuid

FILENAME = "todo_cli.db"

def create_db():
    db = sqlite3.connect(FILENAME)
    curr = db.cursor()
    curr.execute("CREATE TABLE users (id VARCHAR(32) PRIMARY KEY NOT NULL, username VARCHAR(50) NOT NULL, password VARCHAR(16) NOT NULL)")
    curr.execute("""
    CREATE TABLE task (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task VARCHAR(100) NOT NULL, 
        status BOOLEAN DEFAULT 0 NOT NULL, 
        user_id VARCHAR(32),
        FOREIGN KEY (user_id)
        REFERENCES users (id)  )
    """)
    db.commit()
    curr.close()
    return db


def get_user(db, username, password):
    curr = db.cursor()
    user = curr.execute("SELECT * FROM users WHERE username=? AND password=?",(username, password)).fetchone()
    db.commit()
    curr.close()
    return user


def get_user_from_id(db, id):
    curr = db.cursor()
    user = curr.execute("SELECT * FROM users WHERE id=?",(id,)).fetchone()
    db.commit()
    curr.close()
    return user

def create_user(db, username, password):
    curr = db.cursor()
    uid = uuid.uuid4().hex
    curr.execute("INSERT INTO users VALUES (?,?,?)",(uid, username, password))
    curr.close()
    db.commit()

def list_users(db):
    curr = db.cursor()
    users = curr.execute("SELECT username from users")
    for user in users:
        print(user[0])
    curr.close()


def delete_user(db, id):
    with db as curr:
        curr.execute("DELETE FROM users WHERE id=?",(id,))
        curr.execute("DELETE FROM task WHERE user_id=?", (id,))
    db.commit()

def add_task(db, task, user_id):
    with db as curr:
        curr.execute("INSERT INTO task (task, user_id) VALUES (?, ?)",(task, user_id ))
    db.commit()

def list_task(db, user_id):
    res = []
    with db as curr:
        tasks = curr.execute("SELECT id, task, status FROM task WHERE user_id=?",(user_id,))
        for task in tasks:
            res.append(task)
    return res

def delete_task(db, ids):
    with db as curr:
        curr.execute("DELETE FROM task WHERE id IN %s "%str(ids))
    db.commit()

def update_task(db, id, status):
    with db as curr:
        curr.execute("UPDATE task SET status=? WHERE id=?",(status, id))
    db.commit()

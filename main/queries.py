import sqlite3
import uuid
from main.style import bcolors

FILENAME = "database.db"

def create_db():
    db = sqlite3.connect(FILENAME)
    curr = db.cursor()
    curr.execute("""
    CREATE TABLE users (
        id VARCHAR(32) PRIMARY KEY NOT NULL, 
        username VARCHAR(50) NOT NULL,
        password VARCHAR(16) NOT NULL)
        """)
    curr.execute("""
    CREATE TABLE task (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        task VARCHAR(100) NOT NULL, 
        status BOOLEAN DEFAULT 0 NOT NULL,
        expired BOOLEAN DEFAULT 0,
        deadline INTEGER,
        user_id VARCHAR(32),
        FOREIGN KEY (user_id)
        REFERENCES users (id)  )
    """)
    curr.execute("""
    CREATE TABLE commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        command TEXT NOT NULL,
        createdAt INTEGER NOT NULL,
        deadline INTEGER NOT NULL,
        user_id VARCHAR(32),
        FOREIGN KEY (user_id)
        REFERENCES users (id))
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
    from todo import current_user
    curr = db.cursor()
    users = curr.execute("SELECT id, username from users")
    for user in users:
        name =  bcolors.OKBLUE+user[1]+bcolors.ENDC if user[0] == current_user else user[1]
        print(name, end=", ")
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

def list_task(db, user_id, only):
    todo_query = "SELECT id, task, status, 'todo' FROM task WHERE user_id=?"
    cmd_query = "SELECT id, command, deadline, 'cmd' FROM commands WHERE user_id=?"
    res = []
    with db as curr:
        if not only:
            tasks = curr.execute(f"{todo_query} UNION {cmd_query}",(user_id,user_id))
        elif only == "todo":
            tasks = curr.execute(todo_query, (user_id,))
        elif only == "cmd":
            tasks = curr.execute(cmd_query, (user_id,))
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

def get_commands():
    db = sqlite3.connect(FILENAME)
    with db as curr:
        rows = curr.execute("SELECT * FROM commands")
    db.commit()
    return rows

def add_commands(db, command, createdAt, deadline, user_id=0):
    with db as curr:
        curr.execute("INSERT INTO commands (command, createdAt, deadline, user_id) VALUES (?, ?, ?, ?)",(command, createdAt, deadline, user_id))
    db.commit()
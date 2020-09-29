import sys
import sqlite3
import argparse
import hashlib
import os

USERNAME = None
PASSWORD = None
FILENAME = "todo_cli.db"


def create_db():
    db = sqlite3.connect(FILENAME)
    curr = db.cursor()
    curr.execute("CREATE TABLE users (id INT PRIMARY KEY , username VARCHAR(50) NOT NULL, password VARCHAR(16) NOT NULL)")
    curr.execute("CREATE TABLE task (id INT PRIMARY KEY, task VARCHAR(100) NOT NULL, status BOOLEAN DEFAULT 0 NOT NULL )")
    db.commit()
    curr.close()
    return db


if not os.path.exists(FILENAME):
    db = create_db()
else:
    db = sqlite3.connect(FILENAME)

def get_user(id):
    curr = db.cursor()
    user = curr.execute("SELECT username, password FROM users WHERE ID=?",(id,))
    db.commit()
    curr.close()
    
    return user.fetchone()



def create_user(username, password):
    curr = db.cursor()
    curr.execute("INSERT INTO users VALUES (NULL,?,?)",(username, password))
    curr.close()
    db.commit()


def arg_pasers():
    parser = argparse.ArgumentParser(description="Todo Management in CLI.", prog="TODO-CLI")
    sub_parsers = parser.add_subparsers(dest="mode")
    register_parser = sub_parsers.add_parser("register", help="creates a user")
    register_parser.add_argument("-u", "--username", dest='username', type=str, help='Input your username.')
    register_parser.add_argument("-p", "--password", dest="password", type=str, help="Input your passowrd.")
    login_parser = sub_parsers.add_parser("login", help="login a user")
    login_parser.add_argument("-u", "--username", dest='username', type=str, help='Input your username.')
    login_parser.add_argument("-p", "--password", dest="password", type=str, help="Input your passowrd.")
    parser.add_argument("-a","--add", dest="add", help="Adds a task to the todo-list")
    args = parser.parse_args()
    main(args)


def main(args):
    if args.mode == "login":
        sys.stdout.write(get_user(1)) 
    elif args.mode == 'register':
        create_user(username=args.username, password=args.password)



    

if __name__ == "__main__":
    arg_pasers()
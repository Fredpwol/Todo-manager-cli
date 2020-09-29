import sys
import sqlite3
import argparse
import hashlib
import os
import queries

USERNAME = None
PASSWORD = None
FILENAME = "todo_cli.db"


if not os.path.exists(FILENAME):
    db =  queries.create_db()
else:
    db = sqlite3.connect(FILENAME)


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
        sys.stdout.write(queries.get_user(db,1)) 
    elif args.mode == 'register':
        queries.create_user(db,username=args.username, password=args.password)



    

if __name__ == "__main__":
    arg_pasers()
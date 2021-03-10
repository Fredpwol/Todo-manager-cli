#!/usr/bin/python3

import sys
import sqlite3
import argparse
import hashlib
import os
import shelve
import getpass
import subprocess
import time
from main.style import bcolors, strike
from main import queries, session, FILENAME

with shelve.open(session) as p:
    current_user = p.get('user', None)

if not os.path.exists(FILENAME):
    db = queries.create_db()
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
    del_parser = sub_parsers.add_parser("del", help="delete a user account")
    del_parser.add_argument("-u", "--username", dest='username', type=str, help='Input your username.')
    del_parser.add_argument("-p", "--password", dest="password", type=str, help="Input your passowrd.")
    parser.add_argument("-a ", "--add ", dest="add", help="Adds a task to the todo-list", type=str)
    parser.add_argument("--cmd ", dest="cmd", help="A command that will be run", type=str)
    parser.add_argument("--set", dest="set", help="update a task to the todo-list", type=int)
    parser.add_argument("-s", dest="status", help="status of a task", type=str)
    parser.add_argument("-rm", dest="rm", help="removes a task with the curresponding number in the task list", type=int, nargs='+')
    parser.add_argument("--cusr", help="gets the current logged in user", action="store_true")
    parser.add_argument("--clear", help="remove all task", action="store_true", default=False)
    parser.add_argument("-t", "--tasks", dest='tasks', help="list all task currently available", action="store_true")
    parser.add_argument('--only', help="specify if to view only todo task or command task valid argument are 'cmd' and 'todo'", type=str)
    sub_parsers.add_parser("users", help="A list of all users registed to todo-cli on current computer")
    parser.add_argument("--sec", help="seconds", type=int)
    parser.add_argument("--min", help="minutes", type=int)
    parser.add_argument("--hrs", help="hours", type=int)
    parser.add_argument("--days", help="days", type=int)
    args = parser.parse_args()
    main(args)


def main(args):
    if args.mode: 
        if args.mode == "login":
            if (not (args.username or args.password)):
                username = input("Enter your username > ")
                password = getpass.getpass("Enter your password > ")
            else:
                username = args.username
                password = args.password
            user = queries.get_user(db, username=username, password=password)
            print()
            if user:
                uid = user[0]
                with shelve.open(session) as p:
                    p['user'] = uid
            else:
                print(bcolors.FAIL+"Invalid login details!"+bcolors.ENDC)
        elif args.mode == 'register':
            if (not (args.username or args.password)):
                username = input("Enter your username > ")
                password = getpass.getpass("Enter your password > ")
            else:
                username = args.username
                password = args.password
            
            null_value = "username" if not username else "password" if not password else ""
            if null_value:
                print("%s can't be null"%null_value)
            else:
                queries.create_user(db, username=username, password=password)
                print(bcolors.OKGREEN+"User created!!"+bcolors.ENDC)

        elif args.mode == 'users':
            queries.list_users(db)

        elif args.mode == "del":
            if (not (args.username or args.password)):
                username = input("Enter your username > ")
                password = getpass.getpass("Enter your password > ")
            else:
                username = args.username
                password = args.password
            user = queries.get_user(db, username=username, password=password)
            print()
            if user:
                id = user[0]
                inp = None
                while not inp:
                    text = bcolors.WARNING + "Are you sure you want to delete %s y/n ? "%username + bcolors.ENDC
                    inp = input(text)
                if inp.lower() == 'y':
                    queries.delete_user(db, id)
                    if current_user == id:
                        with shelve.open(session) as p:
                            p["user"] = None
            else:
                print(bcolors.FAIL+"Invalid login details!"+bcolors.ENDC)
    else:
        if args.cusr:
            if current_user:
                user = queries.get_user_from_id(db, current_user)
                if user:
                    print(user[1])
        elif args.add:
            queries.add_task(db, args.add, current_user)
        elif args.tasks:
            if args.only and not args.only in ["todo", "cmd"]: 
                raise TypeError("%s is not a valid argument use either cmd or todo"%args.only)
            print("\n"+"S/N", "task", sep="\t")
            print("==========================")
            for i, (_, task, status, type) in enumerate(queries.list_task(db,current_user, args.only)):
                if type == "todo" and status:
                    # task = bcolors.DIM+task+bcolors.ENDC
                    if sys.platform.lower() != 'win32':
                        task = strike(task)
                if type == "cmd":
                    if time.time() > status:
                        task = bcolors.FAIL+task+bcolors.ENDC
                    else:
                        task = bcolors.OKGREEN+task+bcolors.ENDC
                else:
                    task = bcolors.WARNING+task+bcolors.ENDC
                print(i, task, sep="\t")
        elif args.clear:
            state = ""
            while not state.lower() in ['y', 'n']: 
                state = input("Are you sure you want to clear tasks? y/n > ")
            if state.lower() == "y":
                queries.clear_tasks(db)
            return
        elif args.rm:
            if len(args.rm) > 1:
                ids = []
                for n in args.rm:
                    id = queries.list_task(db, current_user)[n][0]
                    ids.append(id)
            
                ids = tuple(ids)
            else:
                ids = '(%s)'%queries.list_task(db, current_user)[args.rm[0]][0]
            queries.delete_task(db, ids)
        elif args.set:
            if args.status:
                id = queries.list_task(db, current_user)[args.set][0]
                queries.update_task(db, id, args.status)
            else:
                print("Input status")
        elif args.cmd:
            exc_time = 0
            if args.sec:
                exc_time += args.sec
            if args.min:
                min = args.min * 60
                exc_time += min
            if args.hrs:
                hrs = args.hrs * 60 * 60
                exc_time += hrs
            if args.days:
                days = args.days * 24 * 60 * 60 
                exc_time += days

            createdAt = time.time()+1
            deadline = createdAt + exc_time
            queries.add_commands(db, args.cmd, createdAt, deadline, current_user)
            os.system("pkill -f task_scheduler.py")
            FILE_PATH = os.path.dirname(__file__)
            os.system("nohup python3 -u %s/task_scheduler.py &"%FILE_PATH)



    

if __name__ == "__main__":
    arg_pasers()
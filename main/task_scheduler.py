#!/usr/bin/env python3

import sched
import time
import queries
import datetime
import subprocess
import multiprocessing

event_scheduler = sched.scheduler(time.time, time.sleep)


def read_code(cmd):
    """
    Receives commands and executes it.
    """
    shell = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    shell_out,shell_err = shell.communicate()
    msg = str(shell_out.decode('utf-8')) + str(shell_err.decode('utf-8'))
    print(msg)

queue = []
def run_scheduler():
    commands = queries.get_commands()
    for cmd in commands:
        if not cmd[0] in queue:
            if time.time() <= cmd[3]:
                event_scheduler.enterabs(cmd[3], 1, read_code, argument=(cmd[1],))
                queue.append(cmd[0])
                # if (e in event_scheduler.queue): event_scheduler.cancel(e)
    event_scheduler.run(blocking=True)

while True:
    p = multiprocessing.Process(target=run_scheduler)
    p.start()
    p.join()

#TODO : Resolve running task parrallel
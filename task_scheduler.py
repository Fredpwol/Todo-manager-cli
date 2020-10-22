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
    Receives commands and executes it afterwards sends it to the server.
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

# event_scheduler.enter(10, 1, lambda: print("hello"))
# event_scheduler.enter(15, 1, lambda: print("world!"))
# event_scheduler.enterabs(time.time()-19, 1, lambda: print("!!!"))
# event_scheduler.run()
import sched
import time
from main import queries
import datetime
import subprocess
import multiprocessing
import signal
from concurrent.futures import ThreadPoolExecutor




def read_code(cmd):
    """
    Receives commands and executes it.
    """
    shell = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    shell_out,shell_err = shell.communicate()
    msg = str(shell_out.decode('utf-8')) + str(shell_err.decode('utf-8'))
    print(msg)

queue = []


def add_task(task):
    event_scheduler = sched.scheduler(time.time, time.sleep)
    if not task[0] in queue:
        if time.time() <= task[3]:
            event_scheduler.enterabs(task[3], 1, read_code, argument=(task[1],))
            queue.append(task[0])

            event_scheduler.run(blocking=True)
            
def run_scheduler():
    commands = queries.get_commands()
    with ThreadPoolExecutor() as pool:
        pool.map(add_task, commands)

while True:
    run_scheduler()

#TODO : Resolve running task parrallel
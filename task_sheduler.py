import sched
import time
import queries
import datetime

event_sheduler = sched.scheduler(time.time, time.sleep)

commands = queries.get_commands()
for cmd in commands:
    date = datetime.datetime
    print("deadline: ", date.fromtimestamp(cmd[2]), "createdAt: ", date.fromtimestamp(cmd[3]))
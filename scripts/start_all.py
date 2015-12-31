import subprocess
import os
from mailer import gmail
import time

home = os.getenv('TT_HOME')

realtime_master = "bash " + home + "/collect/scripts/realtime_master.sh"
realtime_alive = "bash " + home + "/collect/scripts/realtime_alive.sh"
realtime_stop = "bash " + home + "/collect/scripts/realtime_stop.sh"

def call(cmd,output=True):
	if output:
		return subprocess.call(cmd.strip().split(" "))
	else:
		return subprocess.check_output(cmd.strip().split(" ")).decode('utf-8')

time.sleep(3)
call(realtime_master)
time.sleep(3)

i = 0
while True:
	time.sleep(60)
	p = call(realtime_alive,False)
	if i == 10:
		gmail("ps checker",p)
		i = 0
	else:
		i = i + 1

import subprocess
import os
from mailer import gmail
import time

home = os.getenv('TT_HOME')

realtime_master = "bash " + home + "/collect/scripts/realtime_master.sh"
realtime_alive = "bash " + home + "/collect/scripts/realtime_alive.sh"
realtime_stop = "bash " + home + "/collect/scripts/realtime_stop.sh"

def call(cmd,output=False):
	if not output:
		return subprocess.call(cmd.strip().split(" "))
	else:
		return subprocess.check_output(cmd.strip().split(" ")).decode('utf-8').strip()

call(realtime_stop)
time.sleep(3)
call(realtime_master)
time.sleep(3)

while True:
	time.sleep(10)
	i = call(realtime_alive,True)
	print(i)
	if i == "0":
		gmail("ps checker","ps is down")
		break

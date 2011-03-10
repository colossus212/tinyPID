from time import time
from tinyPID import *

def esum(pid):
    pid.com.write("gpe")
    e = pid.com.readlines()[0]
    if len(e) == 3:
        return -1 * to_word(ord(e[1]),+ord(e[2]))
    else:
        return to_word(ord(e[0]), ord(e[1]))

def step(pid, y, count):
	x = []
	y = []
	t = []
	t0 = time.time()
	pid.y = y
	for i in range(count):
		x[i] = pid.x
		t[i] = time() - t0
		y[i] = pid.y
	
	return(t, x, y)
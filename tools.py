from time import time
from tinyPID import *

def debug(pid):
    pid.com.write("gd")
    e = pid.com.readlines()[0]
    # receives: 2B esum, and pterm, iterm, dterm 4B each
    # all values are absolute positive
    e = map(ord, e)
    
    dword = lambda a,b,c,d: (to_word(a, b)<<16)+to_word(c, d)
    
    esum = to_word(e[0], e[1])
    pterm = dword(e[2], e[3], e[4], e[5])
    iterm = dword(e[6], e[7], e[8], e[9])
    dterm = dword(e[10], e[11], e[12], e[13])
    
    print "esum: %i" % esum
    print "pterm: %i (unscaled: %i)" % (pterm, pterm/SCALING_FACTOR)
    print "iterm: %i (unscaled: %i)" % (iterm, iterm/SCALING_FACTOR)
    print "dterm: %i (unscaled: %i)" % (dterm, dterm/SCALING_FACTOR)

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
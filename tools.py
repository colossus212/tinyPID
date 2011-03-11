from time import time
from tinyPID import *

def flush(pid):
	pid.com.readlines()

def debug(pid):
	pid.com.write("gd")
	e = pid.com.readlines()[0]
	# receives: yflag, sign, 2B esum, pterm-sign, 4B pterm, sign, iterm, sign, dterm
	# sign is 1 for a following negativ value, otherwise 0
	e = map(ord, e)

	dword = lambda a,b,c,d: (to_word(a, b)<<16)+to_word(c, d)
	sign  = lambda s, v: s and -v or v

	yflag = e[0]
	esign, psign, isign, dsign = e[1], e[4], e[9], e[14]
	
	esum  = sign(esign, to_word(e[2], e[3]))
	pterm = sign(psign, dword(e[5], e[6], e[7], e[8]))
	iterm = sign(isign, dword(e[10], e[11], e[12], e[13]))
	dterm = sign(dsign, dword(e[15], e[16], e[17], e[18]))

	print "error: %i, pv: %i, sp: %i, output: %i" % (pid.e, pid.x, pid.w, pid.y)
	print "esum:", esum
	print "pterm: %i (unscaled: %i)" % (pterm, pterm/SCALING_FACTOR)
	print "iterm: %i (unscaled: %i)" % (iterm, iterm/SCALING_FACTOR)
	print "dterm: %i (unscaled: %i)" % (dterm, dterm/SCALING_FACTOR)

	if yflag == 1:
		print "y is in output range"
	elif yflag == 2:
		print "y > MAX_OUTPUT"
	elif yflag == 0:
		print "y < MIN_OUTPUT"

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
from time import time, sleep
from tinyPID import *

def flush(pid):
	pid.com.readlines()

def debug(pid):
	pid.com.write("gd")
	
	e = pid.com.readlines()[0]
	# receives: sign, 2B esum, pterm-sign, 4B pterm, sign, iterm, sign, dterm
	# sign is 1 for a following negativ value, otherwise 0
	
	print "w: %3i x: %3i e: %3i y: %3i" % (pid.w, pid.x, pid.e, pid.y)
	
	if len(e) == 18:
		e = map(ord, e)

		dword = lambda a,b,c,d: (to_word(a, b)<<16)+to_word(c, d)
		sign  = lambda s, v: s and -v or v

		esign, psign, isign, dsign = e[0], e[3], e[8], e[13]
		
		esum  = sign(esign, to_word(e[1], e[2]))
		pterm = sign(psign, dword(e[4], e[5], e[6], e[7]))
		iterm = sign(isign, dword(e[9], e[10], e[11], e[12]))
		dterm = sign(dsign, dword(e[14], e[15], e[16], e[17]))

		print "---------------------------"
		print " esum: %4i" % esum
		print "pterm: %4i (unscaled: %3i)" % (pterm, pterm/SCALING_FACTOR)
		print "iterm: %4i (unscaled: %3i)" % (iterm, iterm/SCALING_FACTOR)
		print "dterm: %4i (unscaled: %3i)" % (dterm, dterm/SCALING_FACTOR)
		print "---------------------------"
	else:
		print e
	
	print pid.opmode == 'm' and 'Manual mode.' or 'Auto mode.'



def stepresponse(pid, y0=0, y1=255, count=1000):
	pid.y = y0
	x = []
	y = []
	t = []
	t0 = time()
	pid.y = y1
	for i in range(count):
		x.append(pid.x)
		t.append(time() - t0)
		y.append(pid.y)
	
	return(t, x, y)
	
def log(pid, interval=1):
	try:
		while True:
			w, x, y = pid.w, pid.x, pid.y
			e = w - x
			print "w: %3i, x: %3i, e: %3i, y: %3i" % (w, x, e, y)
			sleep(interval)
		
	except KeyboardInterrupt:
		return
		
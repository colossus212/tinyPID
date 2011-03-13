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


def info(pid):
	p, i, d = pid.Kp, pid.Ki, pid.Kd
	v, n = Kd_to_Tv(p, d), Ki_to_Tn(p, i)
	w, x, y = pid.w, pid.x, pid.y
	xmin, xmax, ymin, ymax = pid.get_limits();
	e = w - x
	m = pid.opmode
	
	print "Kp: %2.2f Ki: %2.2f Kd: %2.2f" % (p, i, d)
	print "Tn: %2.2f Tv: %2.2f" % (n, v)
	print "w: %i x: %i e: %i y: %i" % (w, x, e, y)
	print "x: %i..%i y: %i..%i" % (xmin, xmax, ymin, ymax)
	print m == 'a' and "automatic" or "manual"


def ystepresponse(pid, y0=0, y1=255, count0=500, count1=1000):
	pid.y = y0
	x = []
	y = []
	t = []
	t0 = time()
	for i in range(count0+count1):
		if i == count0:
			pid.y = y1
		x.append(pid.x)
		t.append(time() - t0)
		y.append(pid.y)
	
	return (t, x, y)
	
def wstepresponse(pid, w0=0, w1=255, count0=500, count1=1000):
	pid.auto()
	pid.w = w0
	w = []
	x = []
	y = []
	t = []
	t0 = time()
	for i in range(count0+count1):
		if i == count0:
			pid.w = w1
		t.append(time() - t0)
		x.append(pid.x)
		y.append(pid.y)
		w.append(pid.w)
	
	return (t, x, y, w)
	
def logging(pid, interval=1):
	try:
		while True:
			w, x, y = pid.w, pid.x, pid.y
			e = w - x
			print "w: %3i, x: %3i, y: %3i, e: %3i" % (w, x, y, e)
			sleep(interval)
	except KeyboardInterrupt:
		return

def qplot(t, x=None, y=None, w=None):
	if x is not None:
		plot(t, x, 'r', label='x')
	if y is not None:
		plot(t, y, 'b', label='y')
	if w is not None:
		plot(t, w, 'g', label='w')
	
	legend()
	show()
from time import time, sleep
from matplotlib.pylab import *
from tinyPID import *

def flush(pid):
	pid.com.readlines()

def info(pid):
	p, i, d = pid.Kp, pid.Ki, pid.Kd
	v, n = Kd_to_Tv(p, d), Ki_to_Tn(p, i)
	w, x, y = pid.w, pid.x, pid.y
	ymin, ymax = pid.get_limits();
	e = w - x
	m = pid.opmode
	
	print "Kp: %2.2f \nKi: %2.2f (Tn: %2.2f) \nKd: %2.2f (Tv: %2.2f)" % (p, i, n, d, v)
	print "w: %i \nx: %i \ne: %i \ny: %i (%i..%i)" % (w, x, e, y, ymin, ymax)
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
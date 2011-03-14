#!/usr/bin/env python
#
#
# Frontend to tinyPID
#
# author: Remo Giermann (mo@liberejo.de)
# created: 2011/03/03
#

import serial

SAMPLING_TIME  = 16e-3
SCALING_FACTOR = 128


def to_word(msb, lsb):
	return (msb << 8) + lsb

def to_bytes(word):
	return (word >> 8, word & 0xFF)


def Ki_to_Tn(kp, ki):
    if ki > 0:
        return float(kp)/ki
    else:
        return 0

def Kd_to_Tv(kp, kd):
    if kp > 0:
        return float(kd)/kp
    else:
        return 0

def Tn_to_Ki(kp, tn):
    if tn > 0:
        return kp/tn
    else:
        raise ValueError

def Tv_to_Kd(kp, tv):
    return kp * tv


def pfactor_scale(kp):
	f = SCALING_FACTOR * kp 
	return int(round(f))

def pfactor_unscale(f):
	return f/float(SCALING_FACTOR)

def ifactor_scale(ki):
	f = ki * SCALING_FACTOR * SAMPLING_TIME 
	return int(round(f))

def ifactor_unscale(f):
	return f/(SCALING_FACTOR * SAMPLING_TIME)

def dfactor_scale(kd):
	f = kd * SCALING_FACTOR/SAMPLING_TIME 
	return int(round(f))

def dfactor_unscale(f):
	return f * SAMPLING_TIME/SCALING_FACTOR


class tinyPID (object):

	def __init__(self, *args, **kwargs):
		self.com = serial.Serial(*args, **kwargs)
		if not self.com.getTimeout():
			self.com.setTimeout(2)
	
	def __del__(self):
		del self.com


	def __readc(self, count=1):
		""" Read and return character(s). """
		s = self.com.read(count)
		if len(s) < count:
			return None
		else:
			return s	
	
	def __readb(self, count=1):
		""" Read byte(s) and return integer(s). """
		s = self.__readc(count)
		if s is not None:
			b = map(ord, s)
			if len(b) == 1:
				return b[0]
			else:
				return b
		else:
			return None
			
	def __readw(self, count=1):
		""" Read byte pair(s) MSB, LSB and return integer(s). """
		r = []
		for i in range(0, count):
			b = self.__readb(2)
			if b is not None and len(b) == 2:
				r.append(to_word(b[0], b[1]))
		
		if len(r) == 1:
			return r[0]
		elif len(r) == 0:
			return None
		else:
			return r

	def __write(self, *args):
		""" Write characters/bytes. """
		for s in args:
			if not type(s) in (str, int):
				raise TypeError			
			if type(s) is int:
				s = chr(s)
			self.com.write(s)

	def __writew(self, word):
		""" Write a long number as MSB/LSB-pair. """
		msb, lsb = to_bytes(word)
		self.__write(msb, lsb)
		

	def get_mode(self):
		""" Get operation mode. """
		
		self.__write("gm")
		return self.__readc()

	def get_Kp(self):
		""" Get proportional factor. """
		
		self.__write("gp")
		return pfactor_unscale(self.__readw())

	def get_Ki(self):
		""" Get integral factor. """
		
		self.__write("gi")
		return ifactor_unscale(self.__readw())
        
	def get_Kd(self):
		""" Get derivative factor. """
		
		self.__write("gd")
		return dfactor_unscale(self.__readw())

	def get_pv(self):
		""" Get process value 'x'. """
		
		self.__write("gx")
		return self.__readb()

	def get_setpoint(self):
		""" Get setpoint 'w'. """
		
		self.__write("gv")
		return self.__readb()

	def get_output(self):
		""" Get output value 'y'. """
		
		self.__write("gy")
		return self.__readb()

	def get_limits(self):
		""" Get output limits. """
		
		self.__write("gl")
		return self.__readb(2)

	def get_constants(self):
		""" Get calculation constants sampling time and scaling factor. """
		
		self.__write("gc")
		return self.__readb(2)

	def set_Kp(self, Kp):
		""" Set proportional factor 'Kp'. """
		
		self.__write("sp")
		self.__writew(pfactor_scale(Kp))
        
	def set_Ki(self, Ki):
		""" Set integral factor 'Ki'. """
		
		self.__write("si")
		self.__writew(ifactor_scale(Ki))
	
	def set_Kd(self, Kd):
		""" Set derivative factor 'Kd'. """
		
		self.__write("sd")
		self.__writew(dfactor_scale(Kd))
	
	def set_setpoint(self, w):
		""" Set setpoint 'w'. """
		
		self.__write("sv", w)

	def set_output(self, y):
		""" Set output value 'y' manually. """
		
		self.__write("sy", y)
		
	def set_limits(self, ymin=0, ymax=255):
		""" Set output limits. """
		
		self.__write("sl", ymin, ymax)

	def auto(self):
		""" Set to automatic mode. """
		
		self.__write("a")

	def manual(self):
		""" Set to manual mode. """
		
		self.__write("m")

	def save(self):
		""" Save device configuration to EEPROM. """
		
		self.__write("e")


	def __getattr__(self, name):
		if name == "Kp":
			return self.get_Kp()
		elif name == "Ki":
			return self.get_Ki()
		elif name == "Kd":
			return self.get_Kd()
		elif name == "Tn":
			p, i = self.get_Kp(), self.get_Ki()
			return Ki_to_Tn(p, i)
		elif name == "Tv":
			p, d = self.get_Kp(), self.get_Kd()
			return Kd_to_Tv(p, d)

		elif name == "opmode":
			return self.get_mode()

		elif name == "w" or name == "SP":
			return self.get_setpoint()
		elif name == "x" or name == "PV":
			return self.get_pv()
		elif name == "y":
			return self.get_output()
		elif name == "e":
			return self.w-self.x
		
		elif name in ("ymax, ymin, outmax, outmin"):
			ymin, ymax = self.get_limits()
			if name in ("ymin", "outmin"):
				return ymin
			elif name in ("ymax", "outmax"):
				return ymax
		
		else:
			object.__getattr__(self, name)

	def __setattr__(self, name, value):
		if name == "Kp":
			self.set_Kp(value)
		elif name == "Ki":
			self.set_Ki(value)
		elif name == "Kd":
			self.set_Kd(value)
		elif name == "Tn":
			Ki = Tn_to_Ki(self.get_Kp(), value)
			self.set_Ki(Ki)
		elif name == "Tv":
			Kd = Tv_to_Kd(self.get_Kp(), value)
			self.set_Kd(Kd)
			
		elif name == "w" or name == "SP":
			self.set_setpoint(value)

		elif name == "y":
			self.set_output(value)

		elif name == "opmode":
			if value == 'a':
				self.auto()
			elif value == 'm':
				self.manual()
			elif value == 'o':
				self.stop()
			else:
				raise AttributeError("opmode must be 'a', 'm' or 'o'")
			
		elif name in ("ymax, ymin, outmax, outmin"):
			ymin, ymax = self.get_limits()
			if name in ("ymin", "outmin"):
				ymin = value
			elif name in ("ymax", "outmax"):
				ymax = value
			
			self.set_limits(ymin, ymax)
		
		else:
			object.__setattr__(self, name, value)

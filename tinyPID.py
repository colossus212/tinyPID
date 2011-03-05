#!/usr/bin/env python
#
#
# Frontend to tinyPID
#
# author: Remo Giermann (mo@liberejo.de)
# created: 2011/03/03
#

import serial

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


class tinyPID (object):

    def __init__(self, *args, **kwargs):
        self.com = serial.Serial(*args, **kwargs)
        if not self.com.getTimeout():
            self.com.setTimeout(2)

    def __readc(self, count=1):
        s = self.com.read(count)
        if len(s) < count:
            return None
        else:
            return s
    
    def __readb(self, count=1):
        s = self.__readc(count)
        if s is not None:
            b = map(ord, s)
            if count == 1:
                return b[0]
            else:
                return b
        else: 
            return None

    def __write(self, *args):
        for s in args:
            if not type(s) in (str, int):
                raise TypeError

            if type(s) is int:
                s = chr(s)
            self.com.write(s)

    def get_mode(self):
        self.com.flush()
        self.__write("gm")
        return self.__readc()

    def get_parameters(self):
        self.com.flush()
        self.__write("gp")
        p = self.__readb(3)
        if p is not None:
            p[0] = p[0] / 10.
            return p
        else:
            return None

    def get_initial(self):
        self.com.flush()
        self.__write("gi")
        return self.__readc(), self.__readb()

    def get_pv(self):
        self.com.flush()
        self.__write("gx")
        return self.__readb()

    def get_value(self):
        self.com.flush()
        self.__write("gv")
        return self.__readb()

    def get_output(self):
        self.com.flush()
        self.__write("gy")
        return self.__readb()

    def set_parameters(self, Kp, Ki, Kd):
        self.com.flush()
        self.__write("sp", int(10*Kp), Ki, Kd)

    def set_value(self, w):
        self.com.flush()
        self.__write("sv", w)

    def set_initial(self, mode, value=0):
        self.com.flush()
        self.__write("si", mode, value)

    def set_output(self, value):
        self.com.flush()
        self.__write("sy", value)

    def auto(self):
        self.com.flush()
        self.__write("a")

    def manual(self):
        self.com.flush()
        self.__write("m")

    def stop(self):
        self.com.flush()
        self.__write("o")

    def __getattr__(self, name):
        if name in ("Kp", "Ki", "Kd", "Tn", "Tv"):
            p, i, d = self.get_parameters()
            if name == "Kp":
                return p
            elif name == "Ki":
                return i
            elif name == "Kd":
                return d
            elif name == "Tn":
                return Ki_to_Tn(p, i)
            elif name == "Tv":
                return Kd_to_Tv(p, d)

        elif name in ("InitMode", "InitValue"):
            m, v = self.get_initial()
            if name == "InitMode":
                return m
            else:
                return v

        elif name == "opmode":
            return self.get_mode()

        elif name == "w" or name == "SV":
            return self.get_value()
        elif name == "x" or name == "PV":
            return self.get_pv()
        elif name == "y":
            return self.get_output()
        else:
            object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name in ("Kp", "Ki", "Kd", "Tn", "Tv"):
            p, i, d = self.get_parameters()
            if name == "Kp":
                self.set_parameters(Kp=value, Ki=i, Kd=d)
            elif name == "Ki":
                self.set_parameters(Kp=p, Ki=value, Kd=d)
            elif name == "Kd":
                self.set_parameters(Kp=p, Ki=i, Kd=value)
            elif name == "Tn":
                i = Tn_to_Ki(p, value)
                self.set_parameters(Kp=p, Ki=i, Kd=d)
            elif name == "Tv":
                d = Tv_to_Kd(p, value)
                self.set_parameters(Kp=p, Ki=i, Kd=d)

        elif name == "w":
            self.set_value(value)

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

        elif name in ("InitMode", "InitValue"):
            m, v = self.get_initial();
            if name == "InitMode":
                self.set_initial(mode=value, value=v)
            else:
                self.set_initial(mode=m, value=value)

        else:
            object.__setattr__(self, name, value)

        

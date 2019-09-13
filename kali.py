#!/usr/bin/python

import smbus
import math
import numpy as np
import time
import os
import keyboard
import curses
from configparser import SafeConfigParser

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)
stdscr.nodelay(True)




power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)









    

    
#Achsenkalibrierung
    

    
key =''

stdscr.addstr(0,0,"in horizontaler Lage stillhalten, bitte. Weiter mit Q")
stdscr.refresh()

while key != ord('q') :
    key = stdscr.getch()


time.sleep(2)

stdscr.addstr(1,0,"erstelle Z-Achse-Vektor!")
stdscr.refresh()

t_end = time.time() + 5
ZVEC = np.array([0,0,0])
ACC = np.array([read_word_2c(0x3b),read_word_2c(0x3d),read_word_2c(0x3f)])
N = 0


while t_end > time.time():

    ACC = np.array([read_word_2c(0x3b),read_word_2c(0x3d),read_word_2c(0x3f)])
    ZVEC = ZVEC + ACC
    N = N + 1

stdscr.addstr(2,0,"erstellt!")
stdscr.refresh()

ZVEC= ZVEC / N
ZVEC= ZVEC / np.sqrt(np.sum(ZVEC**2))

stdscr.addstr(3,0,"nach vorne kippen, bitte. Weiter mit Q")
stdscr.refresh()

key =''
while key != ord('q'):
    key = stdscr.getch()

stdscr.addstr(4,0,"stillhalten, bitte")
stdscr.refresh()

HVEC = np.array([0,0,0])
t_end = time.time() + 5
N = 0

while t_end > time.time():
    
    ACC = np.array([read_word_2c(0x3b),read_word_2c(0x3d),read_word_2c(0x3f)])
    HVEC= HVEC + ACC
    N = N + 1
    

HVEC = HVEC / N
HVEC= HVEC / np.sqrt(np.sum(HVEC**2))


YVEC = np.cross(ZVEC,HVEC) * - 1
YVEC= YVEC / np.sqrt(np.sum(YVEC**2))



XVEC = np.cross(ZVEC,YVEC)
XVEC= XVEC / np.sqrt(np.sum(XVEC**2))
    
    
    
    


AXList = []
AYList = []
AZList = []

Listlenght = 20

AXP = 0
AXM = 0
AYP = 0
AYM = 0
AZP = 0
AZM = 0

key = ''

stdscr.addstr(5,0,"Achsen abschwenken, bitte. Loggen mit L ,weiter mit Q")
stdscr.refresh()

while key != ord('q'):
    
    key = ''
    key = stdscr.getch()
    
    ACC = np.array([read_word_2c(0x3b),read_word_2c(0x3d),read_word_2c(0x3f)])
    AX = np.dot(ACC,XVEC)
    AY = np.dot(ACC,YVEC)
    AZ = np.dot(ACC,ZVEC)
    
    if len(AXList) >= Listlenght:
        AXList.pop(0)
        AYList.pop(0)
        AZList.pop(0)
    

    AXList.append(AX)
    AXListSort = list(AXList)
    AXListSort.sort()
    AXMedian = AXListSort[int(math.floor(len(AXListSort)/2))]
    
    AYList.append(AY)
    AYListSort = list(AYList)
    AYListSort.sort()
    AYMedian = AYListSort[int(math.floor(len(AYListSort)/2))]
    
    AZList.append(AZ)
    AZListSort = list(AZList)
    AZListSort.sort()
    AZMedian = AZListSort[int(math.floor(len(AZListSort)/2))]
    

    
    
    if key == ord('l'):
        
        AXP = max(AXP, AXMedian)
        AXM = min(AXM, AXMedian)
        AYP = max(AYP, AYMedian)
        AYM = min(AYM, AYMedian)
        AZP = max(AZP, AZMedian)
        AZM = min(AZM, AZMedian)
        
        stdscr.addstr(7,0,str(AXP))
        stdscr.addstr(8,0,str(AXM))
        stdscr.addstr(9,0,str(AYP))
        stdscr.addstr(10,0,str(AYM))
        stdscr.addstr(11,0,str(AZP))
        stdscr.addstr(12,0,str(AZM))
        stdscr.refresh()
        
        




stdscr.addstr(14,0,"Rotation um Z-Achse vorbereiten, bitte. Start mit Q")
stdscr.refresh()

key =''
while key != ord('q'):
    key = stdscr.getch()



stdscr.addstr(15,0,"erstelle Z-Gyro-Vektor!")
stdscr.refresh()

t_end = time.time() + 5
ZGYR = np.array([0,0,0])
N = 0


while t_end > time.time():

    GYR = np.array([read_word_2c(0x43),read_word_2c(0x45),read_word_2c(0x47)])
    ZGYR = ZVEC + GYR
    N = N + 1
    
ZGYR = ZGYR / N
ZGYR= ZGYR / np.sqrt(np.sum(ZGYR**2))


stdscr.addstr(16,0,"Rotation um Y-Achse vorbereiten, bitte. Start mit Q")
stdscr.refresh()

key =''
while key != ord('q'):
    key = stdscr.getch()


stdscr.addstr(17,0,"erstelle Y-Gyro-Vektor!")
stdscr.refresh()

t_end = time.time() + 5
YGYR = np.array([0,0,0])
N = 0


while t_end > time.time():

    GYR = np.array([read_word_2c(0x43),read_word_2c(0x45),read_word_2c(0x47)])
    YGYR = YGYR + GYR
    N = N + 1
    
YGYR = YGYR / N
YGYR= YGYR / np.sqrt(np.sum(YGYR**2))

stdscr.addstr(18,0,"erstelle X-Gyro-Vektor!")

XGYR = np.cross(ZGYR,YGYR)
XGYR= XGYR / np.sqrt(np.sum(XGYR**2))
    
    
        
        
        
        

curses.endwin()

XVECX = XVEC[0]
XVECY = XVEC[1]
XVECZ = XVEC[2]

YVECX = YVEC[0]
YVECY = YVEC[1]
YVECZ = YVEC[2]

ZVECX = ZVEC[0]
ZVECY = ZVEC[1]
ZVECZ = ZVEC[2]


XGYRX = XGYR[0]
XGYRY = XGYR[1]
XGYRZ = XGYR[2]

YGYRX = YGYR[0]
YGYRY = YGYR[1]
YGYRZ = YGYR[2]

ZGYRX = ZGYR[0]
ZGYRY = ZGYR[1]
ZGYRZ = ZGYR[2]

config = SafeConfigParser()
config.read('config.ini')

config.set('main', 'XVECX', str(XVECX))
config.set('main', 'XVECY', str(XVECY))
config.set('main', 'XVECZ', str(XVECZ))

config.set('main', 'YVECX', str(YVECX))
config.set('main', 'YVECY', str(YVECY))
config.set('main', 'YVECZ', str(YVECZ))

config.set('main', 'ZVECX', str(ZVECX))
config.set('main', 'ZVECY', str(ZVECY))
config.set('main', 'ZVECZ', str(ZVECZ))

config.set('main', 'AXP', str(abs(AXP)))
config.set('main', 'AXM', str(abs(AXM)))
config.set('main', 'AYP', str(abs(AYP)))
config.set('main', 'AYM', str(abs(AYM)))
config.set('main', 'AZP', str(abs(AZP)))
config.set('main', 'AZM', str(abs(AZM)))

config.set('main', 'XGYRX', str(XGYRX))
config.set('main', 'XGYRY', str(XGYRY))
config.set('main', 'XGYRZ', str(XGYRZ))
config.set('main', 'YGYRX', str(YGYRX))
config.set('main', 'YGYRY', str(YGYRY))
config.set('main', 'YGYRZ', str(YGYRZ))
config.set('main', 'ZGYRX', str(ZGYRX))
config.set('main', 'ZGYRY', str(ZGYRY))
config.set('main', 'ZGYRZ', str(ZGYRZ))

with open('config.ini', 'w') as f:
    config.write(f)

print("Kalibrierung abgeschlossen und gespeichert")




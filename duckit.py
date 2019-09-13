import smbus
import math
import numpy as np
import time
import os
import curses
import pigpio
import Adafruit_ADS1x15
from configparser import SafeConfigParser


adc = Adafruit_ADS1x15.ADS1115()
pi = pigpio.pi()
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)
stdscr.nodelay(True)



ESC1 =  19      #27,PVL
ESC2 =  23      #24,PVR
ESC3 =  27      #19,PHL
ESC4 =  20      #20,PHR



#######################################################             IMU

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

############################################################        initiiere Variablen






AXList = []
AYList = []
AZList = []

Listlenght = 10

TuneStep = 0.01

key = ''

SPX = 0
SPY = 0
SPZ = 0

PgainX = 0
PgainY = 0
PgainZ = 0

IgainX = 0
IgainY = 0
IgainZ = 0

DgainX = 0
DgainY = 0
DgainZ = 0

PGainFactor = 10

GScale = 1000
maxdiff= 10

AXList = []
AYList = []
AZList = []

GXList = []
GYList = []
GZList = []

FPSList = []
LAST = 0
TICK = 0

IX = 0
IY = 0
IZ = 0

thrst = 0

Action = 0
Axis = 0



    
    
#############################################################      lese config

config = SafeConfigParser()
config.read('config.ini')

XVEC = np.array([float(config.get('main', 'XVECX')),float(config.get('main', 'XVECY')),float(config.get('main', 'XVECZ'))])
YVEC = np.array([float(config.get('main', 'YVECX')),float(config.get('main', 'YVECY')),float(config.get('main', 'YVECZ'))])
ZVEC = np.array([float(config.get('main', 'ZVECX')),float(config.get('main', 'ZVECY')),float(config.get('main', 'ZVECZ'))])

XGYR = np.array([float(config.get('main', 'XGYRX')),float(config.get('main', 'XGYRY')),float(config.get('main', 'XGYRZ'))])
YGYR = np.array([float(config.get('main', 'YGYRX')),float(config.get('main', 'YGYRY')),float(config.get('main', 'YGYRZ'))])
ZGYR = np.array([float(config.get('main', 'ZGYRX')),float(config.get('main', 'ZGYRY')),float(config.get('main', 'ZGYRZ'))])

AXP = float(config.get('main', 'AXP'))
AXM = float(config.get('main', 'AXM'))
AYP = float(config.get('main', 'AYP'))
AYM = float(config.get('main', 'AYM'))
AZP = float(config.get('main', 'AZP'))
AZM = float(config.get('main', 'AZM'))

try:

    PgainX = float(config.get('main', 'PgainX'))
    PgainY = float(config.get('main', 'PgainY'))
    PgainZ = float(config.get('main', 'PgainZ'))

    IgainX = float(config.get('main', 'IgainX'))
    IgainY = float(config.get('main', 'IgainY'))
    IgainZ = float(config.get('main', 'IgainZ'))

    DgainX = float(config.get('main', 'DgainX'))
    DgainY = float(config.get('main', 'DgainY'))
    DgainZ = float(config.get('main', 'DgainZ'))
except:
    pass



############################################################### steuerschleife



while key != ord('q'):
    
    TICK = time.perf_counter() - LAST
    
    V = adc.read_adc(0, gain=1) / 11500 *15.8
    
    FPSList.append(TICK)
    FPSListSort = list(FPSList)
    FPSListSort.sort()
    FPS = 1 / FPSListSort[int(math.floor(len(FPSListSort)/2))]
    
    
    LAST = time.perf_counter()
    
    key = stdscr.getch()
    stdscr.erase()
    
    ACC = np.array([read_word_2c(0x3b),read_word_2c(0x3d),read_word_2c(0x3f)])
    
    AX = np.dot(ACC,XVEC)
    
    if AX > 0: 
        AX = AX / AXP
    else:
        AX = AX / AXM
        
    AY = np.dot(ACC,YVEC)
    if AY > 0: 
        AY = AY / AYP
    else:
        AY = AY / AYM
    
    AZ = np.dot(ACC,ZVEC)
    if AZ > 0: 
        AZ = AZ / AZP
    else:
        AZ = AZ / AZM
    
    
    if len(AXList) >= Listlenght:
        AXList.pop(0)
        AYList.pop(0)
        AZList.pop(0)
        GXList.pop(0)
        GYList.pop(0)
        GZList.pop(0)
        FPSList.pop(0)
    

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
    
    
    GYR = np.array([read_word_2c(0x43),read_word_2c(0x45),read_word_2c(0x47)])
    
    GX = np.dot(GYR,XGYR)
    GY = np.dot(GYR,YGYR)
    GZ = np.dot(GYR,ZGYR)


    GXList.append(GX)
    GXListSort = list(GXList)
    GXListSort.sort()
    GXMedian = (GXListSort[int(math.floor(len(GXListSort)/2))] -25) /GScale
    
    GYList.append(GY)
    GYListSort = list(GYList)
    GYListSort.sort()
    GYMedian = (GYListSort[int(math.floor(len(GYListSort)/2))] +30) /GScale
    
    GZList.append(GZ)
    GZListSort = list(GZList)
    GZListSort.sort()
    GZMedian = (GZListSort[int(math.floor(len(GZListSort)/2))] -340) /GScale
    
    
    ANGX = math.degrees(math.atan2(AYMedian, math.sqrt(AZMedian**2 + AXMedian**2)))
    ANGY = -math.degrees(math.atan2(AXMedian, math.sqrt(AZMedian**2 + AYMedian**2)))
    
    ErrX = SPX - ANGX
    ErrY = SPY - ANGY
    ErrZ = SPZ - GZMedian

    IX  =   IX + IgainX * ErrX
    IY  =   IY + IgainY * ErrY
    IZ  =   IZ + IgainZ * ErrZ
    
    
    

    if key == ord('w'):
        thrst = min(100, thrst+1)
        time.sleep(0.05)
        key = ''

    elif key == ord('s'):
        thrst = max(0,thrst-1)
        time.sleep(0.05)
        key = ''
        
    elif key == ord('n'):
        IX = 0
        IY = 0
        IZ = 0
        key = ''
    
    elif key == ord('a'):
        thrst = 0
        time.sleep(0.05)
        key = ''

    elif key == ord('x'):
        Axis = 'x'
        key = ''
        
    elif key == ord('y'):
        Axis = 'y'
        key = ''
        
    elif key == ord('z'):
        Axis = 'z'
        key = ''
        
    elif key == ord('p'):
        Action = 'p'
        key = ''
        
    elif key == ord('i'):
        Action = 'i'
        key = ''
        
    elif key == ord('d'):
        Action = 'd'
        key = ''
        
    elif key == ord('e'):
    
        if Axis == 'x' and Action == 'p':
            PgainX = round(PgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'p':
            PgainY = round(PgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'p':
            PgainZ = round(PgainZ + TuneStep,2)
            
        if Axis == 'x' and Action == 'i':
            IgainX = round(IgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'i':
            IgainY = round(IgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'i':
            IgainZ = round(IgainZ + TuneStep,2)
            
        if Axis == 'x' and Action == 'd':
            DgainX = round(DgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'd':
            DgainY = round(DgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'd':
            DgainZ = round(DgainZ + TuneStep,2)
            
        key = ''
        
        
            
    elif key == ord('r'):
    
        TuneStep = TuneStep * -1
        
        if Axis == 'x' and Action == 'p':
            PgainX = round(PgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'p':
            PgainY = round(PgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'p':
            PgainZ = round(PgainZ + TuneStep,2)
            
        if Axis == 'x' and Action == 'i':
            IgainX = round(IgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'i':
            IgainY = round(IgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'i':
            IgainZ = round(IgainZ + TuneStep,2)
            
        if Axis == 'x' and Action == 'd':
            DgainX = round(DgainX + TuneStep,2)
        elif Axis == 'y' and Action == 'd':
            DgainY = round(DgainY + TuneStep,2)
        elif Axis == 'z' and Action == 'd':
            DgainZ = round(DgainZ + TuneStep,2)
            
        TuneStep = TuneStep * -1
        
        key = ''
    
        
    PVLP    =   (ErrX * PgainX + ErrY * PgainY + ErrZ * PgainZ) / PGainFactor
    PVLI    =   IX + IY
    PVLD    =   -GXMedian * DgainX - GYMedian * DgainY
    PVLC    =   PVLP + PVLI + PVLD
    PVL     =   min(100,max(0,thrst + max(-maxdiff, min(maxdiff, PVLC))))
    
    PVRP    =   (-ErrX * PgainX + ErrY * PgainY - ErrZ * PgainZ) / PGainFactor
    PVRI    =   -IX + IY
    PVRD    =   +GXMedian * DgainX - GYMedian * DgainY
    PVRC    =   PVRP + PVRI + PVRD
    PVR     =   min(100,max(0,thrst + max(-maxdiff, min(maxdiff, PVRC))))
    
    PHLP    =   (ErrX * PgainX -ErrY * PgainY - ErrZ * PgainZ) / PGainFactor
    PHLI    =   IX - IY
    PHLD    =   -GXMedian * DgainX + GYMedian * DgainY
    PHLC    =   PHLP + PHLI + PHLD
    PHL     =   min(100,max(0,thrst +max(-maxdiff, min(maxdiff, PHLC))))
    
    PHRP    =   (-ErrX * PgainX -ErrY * PgainY + ErrZ * PgainZ) / PGainFactor
    PHRI    =   -IX - IY
    PHRD    =   GXMedian * DgainX + GYMedian * DgainY
    PHRC    =   PHRP + PHRI + PHRD
    PHR     =   min(100,max(0,thrst + max(-maxdiff, min(maxdiff, PHRC))))
    
    
    pi.set_servo_pulsewidth(ESC1, 1000 + PVL * 10)
    pi.set_servo_pulsewidth(ESC2, 1000 + PVR * 10)
    pi.set_servo_pulsewidth(ESC3, 1000 + PHL * 10)
    pi.set_servo_pulsewidth(ESC4, 1000 + PHR * 10)

################################################################################### Screen

    stdscr.addstr(1,5,"CrashBangDuck Spencer v1.0")
    stdscr.addstr(1,50,"FPS: " +str(int(FPS)))
    stdscr.addstr(1,60,"Voltage: " +str(round(V,2)))
    
    stdscr.addstr(3,5,"Beschleunigung X: " +str(round(AXMedian,2)))
    stdscr.addstr(4,5,"Beschleunigung Y: " +str(round(AYMedian,2)))
    stdscr.addstr(5,5,"Beschleunigung Z: " +str(round(AZMedian,2)))
    
    stdscr.addstr(3,30,"Y-Neigung: "       +str(round(ANGY,2)))
    stdscr.addstr(4,30,"X-Neigung: "       +str(round(ANGX,2)))
    stdscr.addstr(5,30,"Throttle:  "       +str(round(thrst,2)))
    
    stdscr.addstr(3,50,"X-Rotation: "      +str(round(GXMedian,2)))
    stdscr.addstr(4,50,"Y-Rotation: "      +str(round(GYMedian,2)))
    stdscr.addstr(5,50,"Z-Rotation:  "     +str(round(GZMedian,2)))

    stdscr.addstr(7,7,"PVL:        "       +str(round(PVL,2)))
    stdscr.addstr(8,7,"P-Action:   "       +str(round(PVLP,2)))
    stdscr.addstr(9,7,"I-Action:   "       +str(round(PVLI,2)))
    stdscr.addstr(10,7,"D-Action:  "       +str(round(PVLD,2)))
    
    stdscr.addstr(7,30,"PVR:       "       +str(round(PVR,2)))
    stdscr.addstr(8,30,"P-Action:  "       +str(round(PVRP,2)))
    stdscr.addstr(9,30,"I-Action:  "       +str(round(PVRI,2)))
    stdscr.addstr(10,30,"D-Action: "       +str(round(PVRD,2)))
        
    stdscr.addstr(12,7,"PHL:       "       +str(round(PHL,2)))
    stdscr.addstr(13,7,"P-Action:  "       +str(round(PHLP,2)))
    stdscr.addstr(14,7,"I-Action:  "       +str(round(PHLI,2)))
    stdscr.addstr(15,7,"D-Action:  "       +str(round(PHLD,2)))
    
    stdscr.addstr(12,30,"PHR:      "       +str(round(PHR,2)))
    stdscr.addstr(13,30,"P-Action  "       +str(round(PHRP,2)))
    stdscr.addstr(14,30,"I-Action: "       +str(round(PHRI,2)))
    stdscr.addstr(15,30,"D-Action: "       +str(round(PHRD,2)))
    
    stdscr.addstr(17,7,"PgainX:     "       +str(PgainX))
    stdscr.addstr(18,7,"PgainY:     "       +str(PgainY))
    stdscr.addstr(19, 7,"PgainZ:    "       +str(PgainZ))
    stdscr.addstr(17,25,"IgainX:    "       +str(IgainX))
    stdscr.addstr(18,25,"IgainY:    "       +str(IgainY))
    stdscr.addstr(19,25,"IgainZ:    "       +str(IgainZ))
    stdscr.addstr(17,43,"DgainX:    "       +str(DgainX))
    stdscr.addstr(18,43,"DgainY:    "       +str(DgainY))
    stdscr.addstr(19,43,"DgainZ:    "       +str(DgainZ))
    
    stdscr.addstr(21,10,"Achsen und Action mit Tasten direkt anwählen! Ausgewählt: " +str(Action) +"gain" +str(Axis))
    stdscr.addstr(22,10,"W/S = Throttle+-, E/D = Gains+-, A = Propeller-Notaus, Q beendet")
    
    
    

pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0)

config.set('main', 'PgainX', str(PgainX))
config.set('main', 'PgainY', str(PgainY))
config.set('main', 'PgainZ', str(PgainZ))
config.set('main', 'IgainX', str(IgainX))
config.set('main', 'IgainY', str(IgainY))
config.set('main', 'IgainZ', str(IgainZ))
config.set('main', 'DgainX', str(DgainX))
config.set('main', 'DgainY', str(DgainY))
config.set('main', 'DgainZ', str(DgainZ))

with open('config.ini', 'w') as f:
    config.write(f)

curses.endwin()


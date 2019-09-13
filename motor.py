import keyboard
import pigpio
import time
import mouse
import curses


pi = pigpio.pi()
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)
stdscr.nodelay(True)


ESC1 =  27      #27,PVL
ESC2 =  24      #24,PVR
ESC3 =  19      #19,PHL
ESC4 =  20      #20,PHR


stdscr.addstr(10,10,"h=high, n=neutral, l=low, q=quit")

key = ''
while key != ord('q'):
    key = stdscr.getch()
    if key == ord('h'):
            stdscr.addstr(15,15,"high      ")
            pi.set_servo_pulsewidth(ESC1, 2000)
            pi.set_servo_pulsewidth(ESC2, 2000)
            pi.set_servo_pulsewidth(ESC3, 2000)
            pi.set_servo_pulsewidth(ESC4, 2000)
    if key == ord('n'):
            stdscr.addstr(15,15,"neutral      ")
            pi.set_servo_pulsewidth(ESC1, 1500)
            pi.set_servo_pulsewidth(ESC2, 1500)
            pi.set_servo_pulsewidth(ESC3, 1500)
            pi.set_servo_pulsewidth(ESC4, 1500)
    if key == ord('l'):
            stdscr.addstr(15,15,"low      ")
            pi.set_servo_pulsewidth(ESC1, 1000)
            pi.set_servo_pulsewidth(ESC2, 1000)
            pi.set_servo_pulsewidth(ESC3, 1000)
            pi.set_servo_pulsewidth(ESC4, 1000)
            
    time.sleep(0.1)

stdscr.erase()
curses.endwin()

pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0)

print("beendet!")

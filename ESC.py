import keyboard
import pigpio
import time

pi = pigpio.pi()

ESC1 =  27
ESC2 =  24
ESC3 =  19
ESC4 =  20

print("q druecken um zu starten")

while True:
    if keyboard.is_pressed('q'):
        break
    else:
        pass

time.sleep(1)


pi.set_servo_pulsewidth(ESC1, 2000)
pi.set_servo_pulsewidth(ESC2, 2000)
pi.set_servo_pulsewidth(ESC3, 2000)
pi.set_servo_pulsewidth(ESC4, 2000)


print("throttle auf max, batterie einschalten, piepen abwarten, q drücken!")

while True:
    if keyboard.is_pressed('q'):
        break

time.sleep(1)


pi.set_servo_pulsewidth(ESC1, 1000)
pi.set_servo_pulsewidth(ESC2, 1000)
pi.set_servo_pulsewidth(ESC3, 1000)
pi.set_servo_pulsewidth(ESC4, 1000)

print("piepen abwarten, drone festhalten, dann q drücken! ACHTUNG: motoren drehen!")

while True:
    if keyboard.is_pressed('q'):
        break

time.sleep(1)


pi.set_servo_pulsewidth(ESC1, 1200)
pi.set_servo_pulsewidth(ESC2, 1200)
pi.set_servo_pulsewidth(ESC3, 1200)
pi.set_servo_pulsewidth(ESC4, 1200)

print("zum abschliessen q drücken")

while True:
    if keyboard.is_pressed('q'):
        break

time.sleep(1)


pi.set_servo_pulsewidth(ESC1, 0)
pi.set_servo_pulsewidth(ESC2, 0)
pi.set_servo_pulsewidth(ESC3, 0)
pi.set_servo_pulsewidth(ESC4, 0)

print("motoren konfiguriert")

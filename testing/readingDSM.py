import time
from gpiozero import Button
import RPi.GPIO as GPIO
print("Gestart")

button = Button(17)

x1 = 2500
y1 = 5
x2 = 12500
y2 = 25
m = (y2 - y1) / (x2 - x1) # Gradien
print(m)

start = int(time.time() * 1000000)
lowDuration = 0
while True:
    dif = int(time.time() * 1000000)
    if button.is_pressed:
        lowDuration += 100
        # print("Button is not pressed")
    if (dif - start) >= 30000000:  # 30 sec
        break
    time.sleep(0.0001)
print(lowDuration)
lowRatio = (lowDuration / 30000000) * 100
print(lowRatio)
xPPM = ((lowRatio - 5) / m) + 2500
print("{} ppm".format(round(xPPM, 0)))
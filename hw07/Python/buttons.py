#!/usr/bin/env python3
#Adam Wiesler
#Turns turns GP1_4 on/off depending on one input attatched to GP1_3 


# Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO
import time

#Input Pin names for buttons here, in matched order
buttons = ["GP1_3"]
LEDs = ["GP1_4"]

#Below controls whether outputs should be inverted due to having pulldowns vs pullups ("1" inverts, "0" does not)
invert = [1]


# Map LEDs to buttons, iverting selections to buttons
pinMap = dict(zip(buttons,LEDs))
invertMap = dict(zip(buttons,invert))


#Setup LED pin directions
for x in LEDs[:]:
    GPIO.setup(x, GPIO.OUT)


#setup interrupt handler
def setLEDs(buttonKey):
    GPIO.output(pinMap[buttonKey], abs(GPIO.input(buttonKey)-invertMap[buttonKey]))

    
    

#set button pin direction, attach interrupts:
for x in buttons[:]:
    GPIO.setup(x, GPIO.IN)
    GPIO.add_event_detect(x, GPIO.BOTH, callback=setLEDs)




print("Running, wating for button presses...")

#Code taken from example... No real need to change this as it just needs to keep program alive
try:
    while True:
        time.sleep(100)   # Let other processes run

except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
GPIO.cleanup()
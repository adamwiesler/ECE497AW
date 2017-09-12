#!/usr/bin/env python3
#Adam Wiesler
#Turns 4 LEDs on/off depending on 4 buttons. LEDs are connected to GP1, Buttons to GP0


# Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO
import time

#Input Pin names for buttons here, in matched order
buttons = ["GP0_3","GP0_4","GP0_5","GP0_6"]
LEDs = ["GP1_3","GP1_4","RED","GREEN"]

#Below controls whether outputs should be inverted due to having pulldowns vs pullups ("1" inverts, "0" does not)
invert = [1,0,1,0]


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
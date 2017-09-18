# Homework hw03:

###Part 1:
"python3 tmp101_alert.py" is my version of getting the TMP101s to talk to the beaglebone.

The TMP101 can appear as 3 different addresses on an i2c bus. If the ADDR pin is grounded, it is 0x48. If its floating, its 0x49, and if its pulled to VDD, its 0x4a.
I connected mine such that they are on 0x49 and 0x4a.

NOTE: I decied to use python as it allows me to also control the LED display for a temperature graph without re-writing my LED code.

In addition to setting up interrupts to alert the user when the temperature goes outside a set range (see lines 7 and 9, temperatures are all in F), the TMP101s are running in 12-bit mode.
I also connected up the 8x8 LED matrix and set it up so it as a time-series graph of the two temperature sensors. 


###Part 2:

"python3 etchasketch_LED.py" is an etchascketch that is controlled by 4 buttons connected to GP0 to move around. 

It is connected to an i2c LED display, and thus the size is fixed at 8x8. The LED matrix should mirror the terminal display.
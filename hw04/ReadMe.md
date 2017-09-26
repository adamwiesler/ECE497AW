# Homework hw04:

### Part 1,  Memory Map:

As per the homework assignment, I created a chart showing the memory map for the 5 items listed.  This can be found in the PDF file called "BeagleboneMemoryMap.pdf"

### Part 2,  GPIO vio mmap:

I modified the file given to us such that the two switched control two LEDs the PAUSE button and a button hooked up to GP0_3 were used to control the RED and GREEN onboard LEDs. The pause button is on GPIO port 2, and GP0_3 is on GPIO port 1.  
The beaglebone_gpio.h file was also modified to includ ethe correct GPIO ports and external PINs.

To compile, run `$bone node etchasketch.js #rows #cols`
To execute code, run  `$bone sudo ./gpioThru`

### Part 3 Rotary Encoders:
I modified my etchasketch from last week to be controllable by two rotary encoders connected to Encoder ports 2 and 3.  
To execute this program, run `$bone python3 etchasketch_LED_Encoders.py`

One encoder moves the cursor left and right, the other moves the cursor up and down.


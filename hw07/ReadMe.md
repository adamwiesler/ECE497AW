# Homework hw07:    

### IO delay:

The purspose of these three different pieces of code is to demonstrate how there are different methods of reading and writing to IO.  The three methods are listed below, and the document IOTiming.pdf located in the root directory go into grated detail.

These programs read an input on GP1_3 of the beaglebone blue, and control output GP1_4.

The python method can be run by "sudo python3 Python/buttons.py"

The mmap method is run by "sudo ./mmap/gpioThru"

Finally, running "sudo insmod kernel/gpio_test.ko" inserts the kernal module.



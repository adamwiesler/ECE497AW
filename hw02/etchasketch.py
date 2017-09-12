#!/usr/bin/env python3
#Adam Wiesler
#Etch-A-Sketch controlled with 4 pushbuttons

#get size based on terminal call. Default to 8. Inputs aren't well sanitized
import sys
if len(sys.argv)>2:
    gridSizeRow = int(sys.argv[1]);
    gridSizeCol = int(sys.argv[2]);
else:
    gridSizeRow = 8;
    gridSizeCol = 8;
    
position = [0,0]

print("Rows: ", gridSizeRow, "Cols: ", gridSizeCol)

import time
import curses
# Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO



#Setup buttons and move directions:
buttons = ["PAUSE","GP0_4","GP0_5","GP0_6"]
directions = [[1,0],[-1,0],[0,1],[0,-1]]
GPIOEdges = [GPIO.FALLING, GPIO.RISING,GPIO.FALLING, GPIO.RISING]
buttonPressedVal = [0, 1, 0, 1]
directionMap = dict(zip(buttons,directions))
edgeMap = dict(zip(buttons,GPIOEdges))
pressedMap = dict(zip(buttons,buttonPressedVal))


#setup interrupt handler
def setPosition(buttonKey):
    if (GPIO.input(buttons[1]) == 1) and (GPIO.input(buttons[3]) == 1):
        clear()
        return
    elif (GPIO.input(buttons[0]) == 0) and (GPIO.input(buttons[2]) == 0):
        leave()
        return
    else:
        if GPIO.input(buttonKey) == pressedMap[buttonKey]:
            move(directionMap[buttonKey][0],directionMap[buttonKey][1])
            return
    
#set button pin direction, attach interrupts:
for x in buttons[:]:
    GPIO.setup(x, GPIO.IN)
    GPIO.add_event_detect(x, edgeMap[x], callback=setPosition)

def move(row, col):
    global position
    workingPositon = [position[0]+row,position[1]+col]
    workingPositon[0] = min(gridSizeRow-1,max(0,workingPositon[0]))
    workingPositon[1] = min(gridSizeCol-1,max(0,workingPositon[1]))
    position = workingPositon;
    
    print("Position = ", position)
    
    if (position[0] == workingPositon[0]) and (position[1] == workingPositon[1]):
        return

    return

def clear():
    print("Clearing...")

def leave():
    print("leaving")
    #curses.nocbreak(); stdscr.keypad(0); curses.echo()
    #curses.endwin()
    GPIO.cleanup()
    exit()
    


try:
    while True:
        time.sleep(100)   # Let other processes run

except KeyboardInterrupt:
    print("Cleaning Up")
    GPIO.cleanup()
    leave()
GPIO.cleanup()
exit()



#Setup the display using curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)


pad = curses.newpad(100, 100)
#  These loops fill the pad with letters; this is
# explained in the next section
for y in range(0, 100):
    for x in range(0, 100):
        try:
            pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
        except curses.error:
            pass

#  Displays a section of the pad in the middle of the screen
pad.refresh(0,0, 5,5, 20,75)




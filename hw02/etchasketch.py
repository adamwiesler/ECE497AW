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

#Setup the display using curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#Create first window at top left for instructions:
win1 = curses.newwin(3, 70, 0, 0)
win1.addstr(0, 0, "Use buttons connected to GP0 to move around")
win1.addstr(1, 0, "Pressing GP0_4 and GP0_6 at the same time clears the display.")
win1.addstr(2, 0, "Pressing GP0_3 and GP0_5 at the same time exits the program.")
win1.refresh()

def clear():
    global win2
    global position
    for y in range(0, gridSizeCol+2):
        for x in range(0, gridSizeRow+2):
            try:
                if (x==0 or x == gridSizeRow+1) or (y==0 or y == gridSizeCol+1):
                    win2.addch(y,x, '*')
                else:
                    win2.addch(y,x, ' ')
            except curses.error:
                pass   
    win2.refresh()
    position = [0,0]
    win2.addch(position[0]+1,position[1]+1,'X')
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()


#Create second Window and clear
win2 = curses.newwin(gridSizeRow+2,gridSizeCol+2, 4, 0)
clear()



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
    global win2
    workingPositon = [position[0]+row,position[1]+col]
    workingPositon[0] = min(gridSizeRow-1,max(0,workingPositon[0]))
    workingPositon[1] = min(gridSizeCol-1,max(0,workingPositon[1]))
    position = workingPositon;
    
    
    #if (position[0] == workingPositon[0]) and (position[1] == workingPositon[1]):
    #    return

    #print("Position = ", position)
    win2.addch(position[0]+1,position[1]+1,'X')
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()


    return


def leave():
    #print("leaving")
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    exit()
    


try:
    while True:
        time.sleep(100)   # Let other processes run

except KeyboardInterrupt:
    #print("Cleaning Up")
    GPIO.cleanup()
    leave()
GPIO.cleanup()
exit()

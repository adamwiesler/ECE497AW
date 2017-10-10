#!/usr/bin/env python3
#Adam Wiesler
#Etch-A-Sketch controlled with 4 pushbuttons

#get size based on terminal call. Default to 8. Inputs aren't well sanitized
import sys
import time
import curses
# Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO
import rcpy 
import rcpy.encoder as encoder
import os
import pygame
import random
import colorsys

if len(sys.argv)>2:
    gridSizeRow = int(sys.argv[1]);
    gridSizeCol = int(sys.argv[2]);
else:
    gridSizeRow = 8;
    gridSizeCol = 8;

LCDWidth = 320;
LCDHeight = 240;

pixelHeight = int(LCDWidth/gridSizeCol)
pixelWidth = int(LCDHeight/gridSizeRow)

pixelCount = 0

position = [0,0]

print("Rows: ", gridSizeRow, "Cols: ", gridSizeCol)



#########################################################3
#########################################################3
#########################################################3

class pyLCD:
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        #if disp_no:
            #print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                #print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        pygame.mouse.set_visible(False)
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def test(self):
        # Fill the screen with red (255, 0, 0)
        bckgrnd = (10, 10, 10)
        self.screen.fill(bckgrnd)
        # Update the display
        pygame.display.update()
    def drawRect(self,y,x,height,width,red,green,blue):
        color = (red, green, blue)
        pygame.draw.rect(self.screen, color, (x,y,width,height), 0)
        # Update the display
        pygame.display.update()
#########################################################3
#########################################################3
#########################################################3

LCDdisp = pyLCD()
LCDdisp.test()


rcpy.set_state(rcpy.RUNNING)

def clearLCDDisplay():
    global pixelCount
    pixelCount = 0
    LCDdisp.test()    
def writeLCDPixel(row,col,red,green,blue):
    LCDdisp.drawRect(pixelWidth*col,pixelHeight*row,pixelWidth,pixelHeight,red,green,blue)
    #something
    return
    



#Setup the display using curses
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#Create first window at top left for instructions:
win1 = curses.newwin(3, 70, 0, 0)
win1.addstr(0, 0, "Use Connected Encoders to move around                        ",curses.color_pair(1))
win1.addstr(1, 0, "Connected LCD display should mirror what the terminal shows  ",curses.color_pair(1))
win1.addstr(2, 0, "                                                             ",curses.color_pair(1))
win1.refresh()

def getColor(index,maximum):
    return colorsys.hsv_to_rgb((index%maximum)/maximum,1.0,1.0)

def clear():
    global win2
    global position
    for y in range(0, gridSizeRow+2):
        for x in range(0, gridSizeCol+2):
            try:
                if (x==0 or x == gridSizeCol+1) or (y==0 or y == gridSizeRow+1):
                    win2.addstr(y,x, '*',curses.color_pair(2))
                else:
                    win2.addstr(y,x, ' ',curses.color_pair(2))
            except curses.error:
                pass   
    win2.refresh()
    position = [0,0]
    win2.addstr(position[0]+1,position[1]+1,'X',curses.color_pair(3))
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()

    clearLCDDisplay()
    writeLCDPixel(position[1],position[0],255,255,255)


#Create second Window and clear
win2 = curses.newwin(gridSizeRow+2,gridSizeCol+2, 4, 0)
clear()


def move(row, col):
    global pixelCount
    pixelCount = pixelCount + 1;
    (red,green,blue) = getColor(pixelCount,gridSizeCol+gridSizeRow)
    writeLCDPixel(position[1],position[0],int(red*255),int(green*255),int(blue*255))
    global position
    global win2
    workingPositon = [position[0]+row,position[1]+col]
    workingPositon[0] = min(gridSizeRow-1,max(0,workingPositon[0]))
    workingPositon[1] = min(gridSizeCol-1,max(0,workingPositon[1]))
    position = workingPositon;
    
    
    #if (position[0] == workingPositon[0]) and (position[1] == workingPositon[1]):
    #    return

    #print("Position = ", position)
    win2.addstr(position[0]+1,position[1]+1,'X',curses.color_pair(3))
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()
    
    writeLCDPixel(position[1],position[0],255,255,255)


    return


buttons = ["PAUSE"]

#setup interrupt handler
def setPosition(buttonKey):
    if (GPIO.input(buttons[0]) == 0):
        clear()
        return

#set button pin direction, attach interrupts:
for x in buttons[:]:
    GPIO.setup(x, GPIO.IN)
    GPIO.add_event_detect(x, GPIO.BOTH, callback=setPosition)



def leave():
    #print("leaving")
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    exit()
    

encoderOld2 = 0
encoderOld3 = 0

try:
    while True:
        
        time.sleep(.04)   # Let other processes run
        if rcpy.get_state() == rcpy.RUNNING:
            e2 = encoder.get(2) # read the encoders
            e3 = encoder.get(3)
            if(e2-encoderOld2>=3):
                #print("Encoder 2: ", e2," ", encoderOld2," ", (e2-encoderOld2))
                move(0,1)
                time.sleep(.08)   # Let other processes run
                encoderOld2 = e2
            elif((e2-encoderOld2 <=-3)):
                #print("Encoder 2: ", e2," ", encoderOld2," ", (e2-encoderOld2))
                move(0,-1)
                time.sleep(.08)   # Let other processes run
                encoderOld2 = e2
            if(e3-encoderOld3>=3):
                move(1,0)
                time.sleep(.08)   # Let other processes run
                encoderOld3 = e3
            elif(e3-encoderOld3<=-3):
                move(-1,0)
                time.sleep(.08)   # Let other processes run
                encoderOld3 = e3

except KeyboardInterrupt:
    #print("Cleaning Up")
    GPIO.cleanup()
    leave()
GPIO.cleanup()
exit()

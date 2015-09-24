import cv
import os
import sys
import math
import curses
import signal
import time, datetime

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    sys.exit(0)

def output(img):
    # Print the output
    for x in xrange(img.height):
        for y in xrange(img.width):
            b, g, r = img[x, y]
            value = 0.1145 * b + g * 0.5866 + r * 0.2989
            index = int(math.floor(value / (256.0 / (len(palette)))))

            try:
                stdscr.move(x, y)
                stdscr.addch(palette[index])
            except:
                pass

    stdscr.refresh()

def screenshot(img):
    ts = time.time()
    f = open("termshot" + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), "w")
    for x in xrange(img.height):
        for y in xrange(img.width):
            b, g, r = img[x, y]
            value = 0.1145 * b + g * 0.5866 + r * 0.2989
            index = int(math.floor(value / (256.0 / (len(palette)))))

            try:
                f.write(palette[index])
            except:
                pass
        f.write('\n')

def capture(camera):
    # Capture the image
    img = cv.QueryFrame(camera)

    thumbnail = cv.CreateImage(
            (columns, rows),
            img.depth,
            img.nChannels
    )

    cv.Resize(img, thumbnail)

    return thumbnail

# Start of the application
signal.signal(signal.SIGINT, signal_handler)

stdscr = curses.initscr()
stdscr.keypad(1)
stdscr.nodelay(1)
curses.noecho()
curses.cbreak()


palette = [' ', '.', '.', '/', 'c', '(', '@', '#', '8']
camera = cv.CaptureFromCAM(0)

# Get the width and height from the terminal (console)
(rows, columns) = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

lastScreenshot = 0

while True:

    if time.time() - lastScreenshot > 1:
        img = capture(camera)

    c = stdscr.getch()
    if c == ord('p'):
        screenshot(img)
        lastScreenshot = time.time()
    
    output(img)

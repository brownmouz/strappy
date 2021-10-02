from os.path import exists
import os
from graphics import *
import datetime
import numpy as np
import pandas as pd

WIDTH = 800
HEIGHT = 700
MAX_COL = 255
MIN_COL = 0
USER1 = 'Hayden'
USER2 = 'Monica'

print(USER1, USER2)
history_available = False
max_points = 50

# Read list of users
userlist = 'users.txt'
if exists(userlist):
    with open(userlist) as f:
        users = f.read().split('\n')
        USER1, USER2 = users[0], users[1]
else:
    raise ValueError('No user list ("users.txt") in current directory')
    
print(USER1, USER2)

# If the log file exists, read history to df
logfile = os.path.expanduser('~/inputs.log')

if exists(logfile):
    df = pd.read_csv(logfile, sep='\t')
    history_available = True
else:
    print('No log file found... creating')
    os.system(f'touch {logfile}')
    with open(logfile, mode='w') as f:
        f.write('user\tx\ty\tdatetime\n')
    
def normalise_colour(c):
    if c > MAX_COL:
        c = MAX_COL
    elif c < MIN_COL:
        c = MIN_COL
    return c
        
def generate_rgb(x,y):

    x_proportion = x / WIDTH
    y_proportion = y / HEIGHT
    
    # Increase brightness near the centre of the board
    white = (int((2 - abs(0.5 - x_proportion)) ** 7) 
             + int((2 - abs(0.5 - y_proportion)) ** 7))
    black = normalise_colour(-int(x_proportion * MAX_COL/3) + int(y_proportion * MAX_COL/3))
    
    r = normalise_colour(MAX_COL - int(x_proportion * MAX_COL) - int(y_proportion * MAX_COL) + white - black)
    g = normalise_colour(int(x_proportion * MAX_COL) - int(y_proportion * MAX_COL) + white - black)
    b = normalise_colour(-MAX_COL + int(x_proportion * MAX_COL) + int(y_proportion * MAX_COL) + white - black)
    
    return r,g,b


def main():
    # Set up loading screen to pick a user
    win = GraphWin('Strap.py', WIDTH, HEIGHT)
    win.setBackground('black')
    vLine = Line(Point(int(WIDTH/2), 0), Point(int(WIDTH/2),HEIGHT))
    vLine.setFill('white')
    vLine.setWidth(5)
    vLine.draw(win)

    user1 = Text(Point(WIDTH*0.2, HEIGHT/2), USER1)
    user1.setTextColor('white')
    user1.setStyle('italic')
    user1.setSize(20)
    user1.draw(win)

    user2 = Text(Point(WIDTH*0.8, HEIGHT/2), USER2)
    user2.setTextColor('white')
    user2.setStyle('italic')
    user2.setSize(20)
    user2.draw(win)

    username = ''
    p1 = win.getMouse()
    if p1.getX() <= WIDTH/2:
        username = USER1
    else:
        username = USER2
    
    user1.undraw()
    user2.undraw()
    hLine = Line(Point(0, int(HEIGHT/2)), Point(WIDTH, int(HEIGHT/2)))
    hLine.setFill('white')
    hLine.setWidth(5)
    hLine.draw(win)


    win.setBackground('white')
    #bgImage = Image(Point(WIDTH/2,HEIGHT/2), "/home/hayden/Documents/repos/strappy/background.png")
    #bgImage.draw(win)
    for x in range(0, WIDTH, 10):
        for y in range(0, HEIGHT, 10):
            px = Rectangle(Point(x,y), Point(x+10, y+10))
            r,g,b = generate_rgb(x,y)
            px.setFill(color_rgb(r,g,b))
            px.setWidth(0)
            px.draw(win)

    # Draw recent point history
    if history_available:
        recent_points = df[df.user == username].sort_values('datetime', ascending=False)[:max_points].copy()
        circles = []

        for hist_point in range(len(recent_points)):
            circles.append(Circle(Point(recent_points.iloc[hist_point].x*WIDTH, 
                recent_points.iloc[hist_point].y*HEIGHT), 7))
            circles[-1].setWidth(2)
            intensity = int((hist_point / max_points) * 255)
            circles[-1].setFill(color_rgb(intensity, intensity, intensity))
            circles[-1].draw(win)


    pos = win.getMouse()

    newCircle = Circle(pos, 15)
    newCircle.setFill('white')
    newCircle.draw(win)
 
    with open(logfile, mode='a') as f:
        output = username + '\t' + str(pos.getX()/WIDTH) +\
                '\t' + str(pos.getY()/HEIGHT) + '\t' +\
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        f.write(output)

    win.getMouse()
    win.close() 

main()

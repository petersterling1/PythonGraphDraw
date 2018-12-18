from tkinter import *
import numpy as np
import math
import webbrowser
from random import shuffle
import sys
import os
import subprocess

#unreal file name
openAfter = False
unrealPath = "FPS Study.app"

#Set A - Simple Lines (Display In Order)
graph0 = [(0,250), (500,250)]

graph1 = [(0,150), (500,350)]

graph2 = [(0,200), (250,200), (250,400), (500,400)]

graph3 = [(0,400), (200,166), (400,333), (500,200)]

#Set B - 90 Degree Corners (Display in Random Order)
graph4 = [(0,250), (130,250), (130,110), (230,110), (230,400), (340,400), (340,300), (410,300), (410,180), (290,180), (290,130), (500,130)]

graph5 = [(0,340), (80,340), (80,410), (250,410), (250,280), (100,280), (100,130), (220,130), (220,180), (320,180), (320,230), (410,230), (410,110), (330,110), (330,40), (500,40)]

graph6 = [(0,80), (110,80), (110,150), (230,150), (230,80), (380,80), (380,150), (320,150), (320,210), (320,260), (100,260), (100,440), (260,440), (410,440), (410,320), (500,320)]

#Set C - Obtuse/Accute Corners (Display in Random Order)
graph7 = [(0,230), (110,140), (146,230), (90,310), (200,390), (320,350), (260,280), (360,250), (310,160), (360,60), (430,130), (500,260)]

graph8 = [(0,80), (100,50), (150,140), (80,200), (150,330), (220,310), (160,420), (340,400), (400,410), (390,280), (270,221), (360,170), (410,90), (500,140)]

graph9 = [(0,220), (70,280), (150,270), (120,370), (290,290), (170,200), (140,100), (240,160), (310,80), (400,170), (360,220), (400,350), (340,420), (500,440)]

array = []

firstName = "Unknown"
lastName = "Unknown"

types = {}
types[''.join(str(x) for x in graph0)] = "A-1"
types[''.join(str(x) for x in graph1)] = "A-2"
types[''.join(str(x) for x in graph2)] = "A-3"
types[''.join(str(x) for x in graph3)] = "A-4"
types[''.join(str(x) for x in graph4)] = "B-1"
types[''.join(str(x) for x in graph5)] = "B-2"
types[''.join(str(x) for x in graph6)] = "B-3"
types[''.join(str(x) for x in graph7)] = "C-1"
types[''.join(str(x) for x in graph8)] = "C-2"
types[''.join(str(x) for x in graph9)] = "C-3"

set = "A"
item = 0

SkipCalc = False

logs = []

ASet = [graph0, graph1, graph2, graph3]
BSet = [graph4, graph5, graph6]
CSet = [graph7, graph8, graph9]

shuffle(BSet)
shuffle(CSet)

sys.setrecursionlimit(90000)

canvas_width = 500
canvas_height = 500

can_draw = False

#-- BEGIN Frechet Distance Algorithm ---
#-- Taken from https://gist.github.com/MaxBareiss/ba2f9441d9455b56fbc9

# Euclidean distance.
def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))

def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

""" Computes the discrete frechet distance between two polygonal lines
Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
P and Q are arrays of 2-element arrays (points)
"""
def frechetDist(P,Q):
    if (SkipCalc):
        return 0
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)

#-- End Frechet Distance Algorithm

def paint(event):
    global can_draw
    global message
    global w

    if(not can_draw):
        return

    drawn_coordinates.append((event.x, event.y))
        
    green = "#2EBD39"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    
    oval = w.create_oval(x1, y2, x2, y2, fill='green', outline='red')
    
    if(event.x > 490 and len(drawn_coordinates) > 10 and len(original_coordinates) > 10 and can_draw):
        message.config(text="Please wait... (this may take up to 10 seconds)")
        master.update()
    
        can_draw = False
        calculate_difference()

def lerp(start, end, t):
    return start + t * (end-start)

def lerp_point(p0, p1, t):
    return (lerp(p0[0], p1[0], t), lerp(p0[1], p1[1], t))

def diagonal_distance(p0, p1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    return max(abs(dx), abs(dy));

def round_point(p):
    return (round(p[0]), round(p[1]));

def line(p0, p1):
    distance = diagonal_distance(p0, p1)
    for i in range(0, distance, 1):
        t = 0
        if distance != 0:
            t = i / distance
        point = round_point(lerp_point(p0, p1, t))
        original_coordinates.append(point)
        x1, y1 = (point[0] - 1), (point[1] - 1)
        x2, y2 = (point[0] + 1), (point[1] + 1)
        w.create_oval(x1, y1, x2, y2, fill="#000000")
        
def calculate_difference():
    global original_coordinates
    global drawn_coordinates
    global can_draw
    global logs
    global SkipCalc
    
    try:
        frechest_distance = frechetDist(original_coordinates, drawn_coordinates)
    except IndexError:
        can_draw = True
        return
        
        
    type = types[''.join(str(x) for x in array[item])]
    
    if (not SkipCalc):
        print(type + ": " + str(frechest_distance))
    
    if (not SkipCalc):
        logs.append(type + "," + str(frechest_distance))
    
    w.delete("all")
    
    if (next_task()):
        task_draw()
    else:
        SkipCalc = True
        script_location = os.path.dirname(os.path.realpath(sys.argv[0]))
        with open(script_location + "/" + lastName + " " + firstName + " - LineDraw" + ".csv", 'w') as logfile:
            for entry in logs:
                logfile.write(entry + "\n")
        #subprocess.call([script_location + "/" + unrealPath, "-FirstName=" + firstName, "-LastName=" + lastName])
        if openAfter:
            subprocess.call(["/bin/bash","-c","open \"" + script_location + "/" + unrealPath + "\" --args -FirstName=" + firstName + " -LastName=" + lastName])
        sys.exit()
    
    #master.destroy()
    
    #message = Label(master, text="FD: " + str(round(frechest_distance, 3)))
    #message.place(relx=0.1, rely=0.9)

def next_task():
    global set
    global item
    
    if (set == "A"):
        if (item < 3):
            item = item + 1
            return True
        else:
            item = 0
            set = "B"
            return True
    if (set == "B"):
        if (item < 2):
            item = item + 1
            return True
        else:
            item = 0
            set = "C"
            return True
    if (set == "C"):
        if (item < 2):
            item = item + 1
            return True
        else:
            return False
        
    
    
def task_draw():
    global set
    global item
    global ASet
    global BSet
    global CSet
    global can_draw
    
    global original_coordinates
    global drawn_coordinates
    
    original_coordinates = []
    drawn_coordinates = []
    
    global array
    
    if (set == "A"):
        array = ASet
    elif (set == "B"):
        array = BSet
    else:
        array = CSet
        
    for i in range(0, len(array[item]), 1):
        if(i == len(array[item]) - 1):
            continue
        
        current = array[item][i]
        next = array[item][i + 1]
        line(current, next)
        
    message.config(text="Trace the line below, starting from the left. (Click and hold to draw the line)")
    master.update()
    can_draw = True
        
def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).place(relx=0.3, rely=0.3)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.place(relx=0.43, rely=0.3)
    return entry

def buttonClicked():
    global firstName
    global lastName
    global user1
    global user2
    global user3
    global user4
    firstName = user2.get().replace(" ", "")
    lastName = user4.get().replace(" ", "")
    firstName = firstName.replace("'", "")
    lastName = lastName.replace("'", "")
    firstName = firstName.replace("-", "")
    lastName = lastName.replace("-", "")
    
    user1.destroy()
    user2.destroy()
    user3.destroy()
    user4.destroy()
    button.destroy()
    task_draw()
    
    
master = Tk()
master.title("Line Task")
master.resizable(0, 0)

w = Canvas(master,
           width=canvas_width,
           height=canvas_height) 

           
w.pack(expand=FALSE, fill=BOTH)

w.bind("<B1-Motion>", paint)

message = Label(w, text="Please enter your name.")
message.place(relx=0.018, rely=0.01)

user1 = Label(master, text="First Name:")
user1.place(relx=0.3, rely=0.3)
user2 = Entry(master)
user2.config(width=25)
user2.place(relx=0.44, rely=0.3)

user3 = Label(master, text="Last Name:")
user3.place(relx=0.3, rely=0.35)
user4 = Entry(master)
user4.config(width=25)
user4.place(relx=0.44, rely=0.35)

button = Button(master, text="OK", width=10, command=buttonClicked)
button.place(relx=0.44, rely=0.4)

#task_draw()

mainloop()
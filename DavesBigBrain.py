#!/usr/bin/env python
# coding: utf-8

# In[1]:


__version__ = '2.1.2'
__author__ = 'SanoKei'


# In[2]:


'''Imports'''

from tkinter import Tk, Frame, Canvas, BOTH, ALL, PhotoImage
import tkinter as tk
import configparser
import os
import random
import time
import json
from PIL import Image, ImageTk
from threading import Thread
from win32api import GetMonitorInfo, MonitorFromPoint


# In[3]:


'''Initialize'''

# initialize tkinter
root = Tk()

# get the directory of the file
current_directory = os.getcwd()
davidImgPath = current_directory + '\\resources\\images\\David\\'


# In[4]:


'''Get'''

# get taskbar height
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
barHeight = monitor_area[3]-work_area[3]


# In[5]:


'''David'''

### Images ###

# idle
idleLeft_0 = ["DAVE_IDLE-LEFT_0_0.gif","DAVE_IDLE-LEFT_0_1.gif","DAVE_IDLE-LEFT_0_2.gif","DAVE_IDLE-LEFT_0_3.gif","DAVE_IDLE-LEFT_0_2.gif","DAVE_IDLE-LEFT_0_1.gif"]
idleRight_0 = ["DAVE_IDLE-RIGHT_0_0.gif","DAVE_IDLE-RIGHT_0_1.gif","DAVE_IDLE-RIGHT_0_2.gif","DAVE_IDLE-RIGHT_0_3.gif","DAVE_IDLE-RIGHT_0_2.gif","DAVE_IDLE-RIGHT_0_1.gif"]
moveLeft_0 = ["DAVE_MOVE-LEFT_0_0.gif","DAVE_MOVE-LEFT_0_1.gif"]
moveRight_0 = ["DAVE_MOVE-RIGHT_0_0.gif","DAVE_MOVE-RIGHT_0_1.gif"]

### Animation ###
animation = {
    "idleLeft_0": idleLeft_0, 
    "idleRight_0": idleRight_0, 
    "moveLeft_0": moveLeft_0, 
    "moveRight_0": moveRight_0,
    "moveUp_0": idleLeft_0,
    "moveDown_0": idleRight_0
}


# In[6]:


'''Find Config''' 

configParser = configparser.RawConfigParser()   
configFilePath = r''+os.getcwd()+'\\resources\\config.txt'
configParser.read(configFilePath)


# In[7]:


'''Read from config'''

### window ###
title = str(configParser.get('window', 'title'))
overrideredirect = bool(configParser.get('window', 'overrideredirect'))
top_most = bool(configParser.get('window', 'top_most'))
trans_color = str(configParser.get('window', 'trans_color'))

### david ###
speed = int(configParser.get('david', 'speed'))


# In[8]:


'''Configuration'''

### window ###
root.title(title)
root.overrideredirect(overrideredirect)
# root.attributes('-alpha', 0.1)
root.wm_attributes("-topmost", top_most)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", trans_color)


# In[9]:


'''David Actions'''

def dave_action(action, var, photo, spd):
### move ###
    if("moveRight" in action):
        x = spd * var
        if(x+root.winfo_rootx() >= root.winfo_screenwidth() - photo.width()):
            root.geometry("+{}+{}".format(str(root.winfo_screenwidth() - photo.width() - 1),str(root.winfo_rooty())))
            return True
        else:
            root.geometry("+{}+{}".format(str(x+root.winfo_rootx()),str(root.winfo_rooty())))
            return False
        
    if("moveLeft" in action):
        x = spd * var
        if(root.winfo_rootx() - x <= 0):
            root.geometry("+{}+{}".format(str(1),str(root.winfo_rooty())))
            return True
        else:
            root.geometry("+{}+{}".format(str(root.winfo_rootx() - x),str(root.winfo_rooty())))
            return False
        
    if("moveUp" in action):
        y = spd * var
        if(root.winfo_rooty() - y <= 0):
            root.geometry("+{}+{}".format(str(root.winfo_rootx()),str(1)))
            return True
        else:
            root.geometry("+{}+{}".format(str(root.winfo_rootx()),str(root.winfo_rooty() - y)))
            return False
        
    if("moveDown" in action):
        y = spd * var
        if(y+root.winfo_rooty() >= root.winfo_screenheight() - photo.height()-barHeight):
            root.geometry("+{}+{}".format(str(root.winfo_rootx()),str(root.winfo_screenheight() - photo.height() - barHeight)))
            return True
        else:
            root.geometry("+{}+{}".format(str(root.winfo_rootx()),str(y + root.winfo_rooty())))
            return False


# In[10]:


'''Window Class'''

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
    def createAnimation(self,imagelist,filePath,t,action,slp,spd):
        stop = False
        perFrame = 0
        path = davidImgPath+filePath+"\\"
        # extract width and height info
        photo = PhotoImage(file=path+imagelist[0])
        width = photo.width()
        height = photo.height()
        # create a list of image objects
        giflist = []
        for imagefile in imagelist:
            photo = PhotoImage(file=path+imagefile)
            giflist.append(photo)

        # loop through the gif image objects for a while
        for k in range(0, t):
            for gif in giflist:
                perFrame += 1
                canvas.delete(ALL)
                canvas.create_image(width/2.0, height/2.0, image=gif)
                stop = dave_action(action,perFrame,photo,spd)
                if(stop):
                    action = "idle"
                canvas.update()
                time.sleep(slp)


# In[ ]:


'''Run main window'''

app = Window(root)

# Actions and weights
actions = json.loads(configParser.get("david","actions"))
weights = json.loads(configParser.get("david","weights"))

# Files and animation
file_name = json.loads(configParser.get("david","file_name"))
rand = json.loads(configParser.get("david","rand"))
sleep = json.loads(configParser.get("david","sleep"))

# Create the canvas
canvas = Canvas(width=128, height=128, bg=trans_color, highlightthickness=0)
canvas.create_line(0,240,640,240, fill='blue')
canvas.pack()

while True:
    # random action
    action_rand = random.choices(actions, weights=weights)
    index = actions.index(str(action_rand[0]))
    t = random.choice(range(list(rand)[index])) + 1
    slp = list(sleep)[index]
    spd = random.choice(range(speed)) + 1
    app.createAnimation(animation.get(actions[index]),file_name[index],t,action_rand[0],slp,spd)
        
root.mainloop()


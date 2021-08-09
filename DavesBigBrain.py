#!/usr/bin/env python
# coding: utf-8

# In[ ]:


__version__ = '4.0.3'
__author__ = 'SanoKei'


# In[ ]:


'''Imports'''

from tkinter import Tk, Frame, Canvas, PhotoImage
import tkinter as tk
import configparser
from multiprocessing import Process
import os
import random
import time
import json
import math
from PIL import Image, ImageTk
from threading import Thread
from selenium import webdriver
from win32api import GetMonitorInfo, MonitorFromPoint
from win32com.client import Dispatch
from playsound import playsound


# In[ ]:


'''Initialize'''

# initialize tkinter
root = Tk()

# get the directory of the file
current_directory = os.getcwd()
davidImgPath = current_directory + '\\resources\\images\\David\\'


# In[ ]:


'''Get Stoff'''

# get taskbar height
def get_task_bar_height():
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    return monitor_area[3]-work_area[3]

barHeight = get_task_bar_height()

# get chrome version
def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
chrome_version = str(list(filter(None, [get_version_via_com(p) for p in paths]))[0]).split('.')[0]

# get direction to face david
def get_direction_for_david(action_rand, cords):
    fileName = "move"
    if (math.sqrt((root.winfo_rootx()-cords[0])**2) >= math.sqrt((root.winfo_rooty()-cords[1])**2)):
        fileName += ""
    else:
        fileName += "Y"
    if(cords[0] >= root.winfo_rootx()):
        # right
        fileName += "Right"
    else:
        fileName += "Left"
        
    return fileName
    
# get a random spot on the screen
def get_random_on_screen(width,height):
    x,y = random.choice(range(width - 128)),random.choice(range(height - barHeight - 128))
    return [x,y]

def get_incrim_of_cords(cords,maxFrame):
    new_x = (cords[0] - root.winfo_rootx()) / maxFrame
    new_y = (cords[1] - root.winfo_rooty()) / maxFrame
    return [new_x,new_y]


# In[ ]:


'''David'''

### Images ###

# idle
idleLeft = ["DAVE_IDLE-LEFT_0_0.gif","DAVE_IDLE-LEFT_0_1.gif","DAVE_IDLE-LEFT_0_2.gif","DAVE_IDLE-LEFT_0_3.gif","DAVE_IDLE-LEFT_0_2.gif","DAVE_IDLE-LEFT_0_1.gif"]
idleRight = ["DAVE_IDLE-RIGHT_0_0.gif","DAVE_IDLE-RIGHT_0_1.gif","DAVE_IDLE-RIGHT_0_2.gif","DAVE_IDLE-RIGHT_0_3.gif","DAVE_IDLE-RIGHT_0_2.gif","DAVE_IDLE-RIGHT_0_1.gif"]
moveLeft = ["DAVE_MOVE-LEFT_0_0.gif","DAVE_MOVE-LEFT_0_1.gif"]
moveRight = ["DAVE_MOVE-RIGHT_0_0.gif","DAVE_MOVE-RIGHT_0_1.gif"]
moveYLeft = ["DAVE_MOVE_Y-LEFT_0_0.gif","DAVE_MOVE_Y-LEFT_0_1.gif","DAVE_MOVE_Y-LEFT_0_2.gif","DAVE_MOVE_Y-LEFT_0_3.gif","DAVE_MOVE_Y-LEFT_0_2.gif","DAVE_MOVE_Y-LEFT_0_1.gif",]
moveYRight = ["DAVE_MOVE_Y-RIGHT_0_0.gif","DAVE_MOVE_Y-RIGHT_0_1.gif","DAVE_MOVE_Y-RIGHT_0_2.gif","DAVE_MOVE_Y-RIGHT_0_3.gif","DAVE_MOVE_Y-RIGHT_0_2.gif","DAVE_MOVE_Y-RIGHT_0_1.gif",]
quackLeft = ["DAVE_QUACK-LEFT_0_0.gif","DAVE_QUACK-LEFT_0_1.gif"]
quackRight = ["DAVE_QUACK-RIGHT_0_0.gif","DAVE_QUACK-RIGHT_0_1.gif"]

### Animation ###
animation = {
    "idleLeft": idleLeft, 
    "idleRight": idleRight, 
    "moveLeft": moveLeft, 
    "moveRight": moveRight,
    "moveYLeft": moveYLeft,
    "moveYRight": moveYRight,
    "webRight": idleRight,
    "quackLeft": quackLeft,
    "quackRight": quackRight
}


# In[ ]:


'''Chrome'''

### Chrome to Version ###
version_to_path = {
    "91": current_directory + "\\resources\\chromeDriver\\91_chromedriver.exe",
    "92": current_directory + "\\resources\\chromeDriver\\92_chromedriver.exe",
    "93": current_directory + "\\resources\\chromeDriver\\93_chromedriver.exe"
}


# In[ ]:


'''Find Config''' 

configParser = configparser.RawConfigParser()   
configFilePath = r''+os.getcwd()+'\\config.txt'
configParser.read(configFilePath)


# In[ ]:


'''Read from config'''
### default ###
debug = bool(configParser.get('window', 'debug'))

### window ###
title = str(configParser.get('window', 'title'))
overrideredirect = bool(configParser.get('window', 'overrideredirect'))
top_most = bool(configParser.get('window', 'top_most'))
trans_color = str(configParser.get('window', 'trans_color'))

### david ###
speed = int(configParser.get('david', 'speed'))

### Actions and weights ###
actions = json.loads(configParser.get("david","actions"))
weights = json.loads(configParser.get("david","weights"))

### Files and animation ###
file_name = json.loads(configParser.get("david","file_name"))
rand = json.loads(configParser.get("david","rand"))
sleep = json.loads(configParser.get("david","sleep"))
minval = json.loads(configParser.get("david","minval"))
rick = json.loads(configParser.get("david","url"))


# In[ ]:


'''Configuration'''

### window ###
root.title(title)
root.overrideredirect(overrideredirect)
root.wm_attributes("-topmost", top_most)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", trans_color)


# In[ ]:


'''David Class'''
class David(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill="both", expand=1)
        
    '''Dave Actions'''
    def dave_action(self,action,perFrame,photo,spd,url,perm_x,perm_y,hardPerm):  
        ### move ###
        perm_x += hardPerm[0]
        perm_y += hardPerm[1]
                
        root.geometry("+{}+{}".format(str(int(math.ceil(perm_x))),str(int(math.ceil(perm_y)))))

        return [perm_x,perm_y]

    '''Create the animation of David'''
    def createAnimation(self,imagelist,filePath,perFrame):
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
        gif = giflist[perFrame]
        canvas.delete("all")
        canvas.create_image(width/2.0, height/2.0, image=gif)
        canvas.update()
                
    def createAction(self,imagelist,filePath,perFrame,action,spd,url,perm_x,perm_y,hardPerm):
        path = davidImgPath+filePath+"\\"
        photo = PhotoImage(file=path+imagelist[0])
        if("move" in imagelist[0].lower()):
            return self.dave_action(action,perFrame,photo,spd,url,perm_x,perm_y,hardPerm)
        else:
            self.dave_action(action,perFrame,photo,spd,url,perm_x,perm_y,hardPerm)


# In[ ]:


def mainLoop(david,canvas):
    # random action
    action_rand = random.choices(actions, weights=weights)
    index = actions.index(str(action_rand[0]))
    t = random.choice(range(list(rand)[index])) + int(minval[index])
    slp = list(sleep)[index]
    spd = random.choice(range(speed)) + int(minval[index])
    roll = random.choice(rick)
    startPoint = [root.winfo_rootx(),root.winfo_rooty()]
    perm_x = root.winfo_rootx()
    perm_y = root.winfo_rooty()
    perFrame = 0

    # sterialize animation
    if isinstance(action_rand, list):
        act_rand = action_rand[0]
    else:
        act_rand = action_rand
    ranSoFarAway = get_random_on_screen(root.winfo_screenwidth(),root.winfo_screenheight())
    if("move" in act_rand):
        act_rand = get_direction_for_david(action_rand,ranSoFarAway)
    maxFrame = t * len(animation.get(act_rand))
    hardPerm = get_incrim_of_cords(ranSoFarAway,maxFrame)
    # animation and action main loop
    for perAnimationLoop in range(t):
        for perFrameAnimation in range(len(animation.get(act_rand))):
            perFrame += 1
            david.createAnimation(animation.get(act_rand),file_name[index],perFrameAnimation)
            if("move" in act_rand.lower()):
                [perm_x, perm_y] = david.createAction(animation.get(act_rand),file_name[index],perFrame,act_rand,spd,roll,perm_x,perm_y,hardPerm)  
            else:
                david.createAction(animation.get(act_rand),file_name[index],perFrame,action_rand,spd,roll,perm_x,perm_y,hardPerm)
            time.sleep(slp)


# In[ ]:


'''Run main window'''

# initialize class of David
david = David(root)

# Create the canvas
canvas = Canvas(width=128, height=128, bg=trans_color, highlightthickness=0)
canvas.pack()

while True:
    mainLoop(david,canvas)
root.mainloop()


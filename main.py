# -*- coding: utf-8 -*-

import pyautogui

import re
import os
import subprocess
import sys
import time
import array

import win32api
import win32gui
import win32con

if __name__ == "__main__":
    time.sleep(1)
    screen_x,screen_y = pyautogui.size()

    pyautogui.moveTo(1, 1, duration=1)

    parent_handle = win32gui.FindWindow(None, "calculator")

    if parent_handle == 0 :
        cmd = 'start C:\Windows\System32\calc.exe'
        subprocess.Popen(cmd, shell=True)
        time.sleep(3)
        parent_handle = win32gui.FindWindow(None, "calculator")

    if parent_handle == 0 :
        print(u"sorry, application start error")
        sys.exit()

    if parent_handle > 0 :
        win_x1,win_y1,win_x2,win_y2 = win32gui.GetWindowRect(parent_handle)
        print(u"position:"+str(win_x1)+"/"+str(win_y1))
        apw_x = win_x2 - win_x1
        apw_y = win_y2 - win_y1
        print(u"view size:"+str(apw_x)+"/"+str(apw_y))
        win32gui.SetForegroundWindow(parent_handle)
        titlebar = win32gui.GetWindowText(parent_handle)
        classname = win32gui.GetClassName(parent_handle)


    pyautogui.moveTo(win_x1+40,win_y1+4, duration=1)
    pyautogui.mouseDown(win_x1+40,win_y1+4, button='left')
    pyautogui.moveTo(100,200, duration=1)
    pyautogui.moveTo(110,100, duration=1)
    pyautogui.moveTo(120,300, duration=1)
    pyautogui.moveTo(130,100, duration=1)
    pyautogui.moveTo(140,300, duration=1)
    pyautogui.moveTo(150,100, duration=1)
    pyautogui.moveTo(160,300, duration=1)
    pyautogui.mouseUp(210,200, button='left')
    time.sleep(30)
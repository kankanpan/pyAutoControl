# -*- coding: utf-8 -*-

import eel
from package import *

def action():
    findWindow.findByKeyword()
    guiAction.click()
    while True:
        if findImg.judgeColor():
            break
        eel.sleep(2)
    

#guiInit.init( action )


import pyautogui

def writeAndEnter(location, text, selectAll=True):
    pyautogui.click(x=location[0], y=location[1])
    if selectAll:
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.press('backspace')
    else:
        pyautogui.press('right', presses=20)
        pyautogui.press('backspace', presses=20)
    pyautogui.write(text)
    pyautogui.press('enter')
    return

def click(location):
    pyautogui.click(x=location[0], y=location[1])
    return

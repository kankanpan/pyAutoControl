import pyautogui

def writeAndEnter(location, text):
    pyautogui.click(x=location[0], y=location[1])
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')
    pyautogui.write(text)

    return

import win32gui
import ctypes

def forground( hwnd, keyword ):
    name = win32gui.GetWindowText(hwnd)
    if name.find(keyword) >= 0:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd,1)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        return True

def findByInput():
    keyword = input()
    win32gui.EnumWindows( forground, keyword )
    forWin = win32gui.GetForegroundWindow()
    print( win32gui.GetWindowText(forWin) )
    return

def findByKeyword( keyword ):
    win32gui.EnumWindows( forground, keyword )
    
    forWin = win32gui.GetForegroundWindow()
    ect = win32gui.GetWindowRect(forWin)
    return ect
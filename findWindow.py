import win32gui
import ctypes

def forground( hwnd, _):
    name = win32gui.GetWindowText(hwnd)
    if name.find(keyword) >= 0:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        print('name:')
        print(name)
        return False

def findByInput():
    keyword = input()
    win32gui.EnumWindows( forground, None)

def findByKeyword( keyword ):
    name = win32gui.GetWindowText(hwnd)
    if name.find(keyword) >= 0:
        return name
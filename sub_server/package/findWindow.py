import sys
import os

def getAllWindowMac():
    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    return windowList

# pid = window['kCGWindowOwnerPID']
# windowNumber = window['kCGWindowNumber']
# ownerName = window['kCGWindowOwnerName']
# geometry = window['kCGWindowBounds']
# windowTitle = window.get('kCGWindowName', u'Unknown')

def getForgroundMac():
    curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    curr_app_name = curr_app.localizedName()

    txt = ""
    for window in getAllWindowMac():
        pid = window['kCGWindowOwnerPID']
        if curr_pid == pid:
            activeWindowTitle = window.get('kCGWindowName', u'Unknown')
            break
    return activeWindowTitle

def getWindowGeoMac( ownerName ):
    for window in getAllWindowMac():
        if window['kCGWindowOwnerName'] == ownerName:
            winGeometry = window['kCGWindowBounds']
            break
    geometry = {}
    for k, v in winGeometry.items():
        geometry[k] = v * 2
    return geometry

def findByKeywordMac( keyword ):
    findWindowTitle = ''
    for window in getAllWindowMac():
        ownerName = window['kCGWindowOwnerName']
        windowTitle = window.get('kCGWindowName', u'Unknown')

        if windowTitle == keyword or ownerName == keyword:
            findWindowTitle = ownerName
            break
    return findWindowTitle

def setForgroundMac( ownerName ):
    tmpl = '''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "{}" to true' '''
    script = tmpl.format(ownerName)
    os.system(script)
    return

def getForgroundWin():
    activeWindowTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow());
    return activeWindowTitle

def setForgroundWin( hwnd, keyword ):
    name = win32gui.GetWindowText(hwnd)
    if name.find(keyword) >= 0:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd,1)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        return True

def findByInputWin():
    keyword = input()
    win32gui.EnumWindows( forground, keyword )
    forWin = win32gui.GetForegroundWindow()
    print( win32gui.GetWindowText(forWin) )
    return

def findByKeywordWin( keyword ):
    win32gui.EnumWindows( forground, keyword )

    forWin = win32gui.GetForegroundWindow()
    ect = win32gui.GetWindowRect(forWin)
    return ect


if sys.platform == "darwin":
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )

    getForground = getForgroundMac
    setForground = setForgroundMac
    findByKeyword = findByKeywordMac
    getWindowGeo = getWindowGeoMac
elif sys.platform == "win32":
    import win32gui
    import ctypes

    getForground = getForgroundWin
    setForground = setForgroundWin
    findByInput = findByInputWin
    findByKeyword = findByKeywordWin
else:
    def getActiveWindowTitle():
        return "Unknown"

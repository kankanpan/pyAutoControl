import win32gui

win32gui.EnumChildWindows(win32gui.FindWindow(u"IEFrame",None),lambda x, _: print(str(x)+' : '+win32gui.GetClassName(x)+' : '+win32gui.GetWindowText(x)), None)
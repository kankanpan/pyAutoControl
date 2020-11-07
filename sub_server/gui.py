import tkinter as tk
import time

import actions

class Gui():
    def __init__(self, status={'value': 0}, ep=None):
        self.running = True
        self.status = status
        self.ep = ep

        self.oldStatus = -1

        self.isConnect = False
        self.isRunning = False

        self.windowName = ""

    def init_window(self):
        self.root.geometry("150x80")
        self.root.minsize(width=150, height=100)
        #self.root.maxsize(width=150, height=50)
        self.root.resizable(0, 1)
        self.root.title("pyAutoControl")
        self.root.configure(bg='white')
        self.root.protocol("WM_DELETE_WINDOW",  self.quit)

        self.c = tk.Canvas(self.root, width=150, height=30, bg="white", highlightthickness=0)
        self.c.create_oval(15, 10, 35, 30, fill="red", tag="ramp")
        self.c.create_text(40, 10, text="disconnect", fill="black", anchor='nw', font=("",18), tag="status")

        self.label = tk.Label(self.root, text=self.status.value, font=("",20), bg="white", foreground="black")
        self.b = tk.Button(self.root, text="-- EXIT --", command=self.quit, font=("",20), bg="white", highlightthickness=0)

        self.getWIndow = tk.Button(self.root, text="capture!", command=self.capture, font=("",20), bg="white", highlightthickness=0)

        self.c.pack()
        self.label.pack()
        self.b.pack()
        self.getWIndow.pack()

        self.root.after(10, self._refreshStatus)

    def start(self):
        self.root = tk.Tk()
        self.init_window()

        self.root.after(1000, self._check_to_quit)
        self.root.mainloop()
        del self.root

    def _check_to_quit(self):
        if self.running:
            self.root.after(1000, self._check_to_quit)
        else:
            self.root.destroy()

    def _refreshStatus(self):
        if self.status.value != self.oldStatus:
            text = 'connecting' if self.status.value == 1 else 'disconnect'
            color = 'green' if self.status.value == 1 else 'red'
            self.c.itemconfig("ramp", fill=color)
            self.c.itemconfig("status", text=text)

            self.oldStatus = self.status.value
        self.root.after(1000, self._refreshStatus)

    def quit(self):
        self.running = False

    def capture(self):
        self.status.value += 1
        self.windowName = actions.window_action()
        if self.windowName:
            self.ep.send(self.windowName)
        return

if __name__ == "__main__":
    guiApp = Gui()
    guiApp.start()

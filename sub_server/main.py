import platform
from multiprocessing import Pipe, Value, Process
import os
import time
import ctypes

from gui import Gui
from api.main import Server

PLATFORM = platform.system()
print(PLATFORM)

if __name__ == "__main__":

    ep1, ep2 = Pipe()
    status = Value('i', 0) # 0 disconnecting, 1 connecting

    apiApp = Server(status, ep1)
    apiApp.start(port=8124)

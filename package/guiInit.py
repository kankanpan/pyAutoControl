import eel
import sys

def init(action):
    eel.init('./gui')

    @eel.expose
    def doActionPy():
        action()
    
    @eel.expose
    def statusCheckPy():
        action()

    @eel.expose
    def forceStopPy():
        sys.exit()

    eel.start('hello.html', size=(800, 300))

    return
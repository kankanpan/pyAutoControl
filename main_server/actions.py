import yaml
import codecs
import time
from ws import Websocket
from package import findWindow, findImg, guiAction

def test_action():
    try:
        time.sleep(2)
        return {"message": "success"}
        pass
    except Exception as e:
        return e
        raise

def ss_action(keyword=None):
    try:
        if keyword:
            ss = aplicationSS(keyword)
        else:
            ss = findImg.SS()
        ss64 = findImg.NdarrayToBase64(ss)
        return ss64
    except Exception as e:
        return e

def window_action(timeValue=1):
    try:
        time.sleep(timeValue)
        name = findWindow.getForground()
        return name
    except Exception as e:
        return e

def aplicationSS(keyword):
    ownerName = findWindow.findByKeyword( keyword )
    location = findWindow.getWindowGeo( ownerName )
    findWindow.setForground( ownerName )
    time.sleep(0.1)
    ss = findImg.SS(location['Height'], location['Width'], location['X'], location['Y'])
    return ss

def setItem(item):
    print(item)
    setYaml('item', item)
    return True

def startWS():
    ws = Websocket()
    ws.testLoop()

def getYaml(name):
    try:
        with open(name + '.yaml') as file:
            obj = yaml.load(file, Loader=yaml.Loader)
            return obj
    except Exception as e:
        print(e)
        return None

def setYaml(name, obj={}):
    try:
        with codecs.open(name + '.yaml', 'w', 'utf-8') as f:
            yaml.dump(obj, f, encoding='utf-8', allow_unicode=True)
        return True
    except Exception as e:
        print(e)
        return None

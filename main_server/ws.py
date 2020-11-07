import websocket
import _thread as thread
import time

PATH = 'ws://localhost:8124/ws'

class Websocket():
    def __init__(self):

        websocket.enableTrace(True)
        print("connect sub server")

    def start(self, func=None):
        self.ws = websocket.create_connection(PATH)
        self.receive(func)

    def send(message='test call'):
        self.ws.send(message)
        print("Sent: " + message)

    async def receive(self, func=None):
        result = await ws.recv()
        if func:
            try:
                func()
            except Exception as e:
                print(e)
                self.close()
        print("Receiving: " + result)
        self.Receive()

    def close(self):
        self.ws.close()
        print("Closed websocket")

    async def testLoop(self):
        def test():
            self.send('test')
        self.ws = websocket.create_connection(PATH)
        await self.receive(test)

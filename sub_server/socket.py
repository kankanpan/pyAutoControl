import websocket
import thread
import time

class Websocket():
    def __init__(self):
        PATH = 'http://0.0.0.0:8123/ws_sub'

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(PATH,
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.ws.on_open = self.on_open

    def start(self):
        self.ws.run_forever()

    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())

if __name__ == "__main__":
    ws = Websocket()
    ws.start()
    ws.run_forever()

import asyncio
import websockets
from Dealer import Dealer
import logging
class UIDealer(Dealer):
    class JOB:
        def __init__(self, ws_type,msg):
            # get sentence and response textStream
            self.ws_type = ws_type
            self.msg = msg
            self.statue = 'ACCEPTED'
            pass

        def cancel(self):
            self.statue = 'CANCELLED'


    def __init__(self):
        super().__init__()
        self.SignalWS = websockets.connect("ws://127.0.0.1:8080")
        self.TextWS = websockets.connect("ws://127.0.0.1:8081")
        self.queue = asyncio.Queue()
        # print('UI DEALER INIT' + str(self.SignalWS) + str(self.TextWS))

    async def main_deal_job(self, job):
        print('UI deal job')
        msg = job.msg
        if job.ws_type == "signal":
            websocket = await self.SignalWS
            # async with websockets.connect("ws://127.0.0.1:8080") as websocket:
            if msg == "waiting":
                signal = "waiting"
            elif msg == "listening":
                signal = "listening"
            elif msg == "speaking":
                signal = "speaking"
            else:
                signal = "waiting"
            await websocket.send(signal)
            print("Controller接收到的消息为：",signal)
        elif job.ws_type == "text":
            # async with websockets.connect("ws://127.0.0.1:8081") as websocket:
            websocket = await self.TextWS
            await websocket.send(msg)
            print("Controller接收到的字幕为：",msg)

    async def deal_job(self, job):
        print('UI DEAL RECEIVED JOB' , job)
        try:
            await self.main_deal_job(job)
        except Exception as e:
            print(e)
            job.statue = 'FAILED'



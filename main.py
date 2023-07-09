from NLPDealer import NLPDealer
from TTSDealer import TTSDealer
from AudioDealer import AudioDealer
from DealerChain import DealerChain
from UIDealer import UIDealer
class AICaller:
    def __init__(self):
        # self.ws_audio_dealer = WSAudioDealer()
        # self.asr_dealer = ASRDealer()
        print("START")
        self.nlp_dealer = NLPDealer()
        self.tts_dealer = TTSDealer()
        self.audio_dealer = AudioDealer()
        self.ui_dealer = UIDealer()
        self.dealchain = DealerChain(self.nlp_dealer,self.tts_dealer,self.audio_dealer,self.ui_dealer)
        print("INIT")

    # async def main_dealing_textStream_to_AudioStream(websocket):
    #     '''
    #     args:
    #         InputTextStream: TextStream(User Input Text Stream)
    #     '''

    #     await wsaudio.add_job(wsaudio.Job(websocket, audioStream))
    #     await asr_dealer.add_job(asr_dealer.Job(textStream, websocket))
    #     while True: 
            
    #         await textstream . get( 'user input')
    #         nlp_dealer . cancel_job( ... )
    #         tts_dealer . cancel_job( ... )
    #         Audio_player . cancel_job( ... )
    #         sentece = await textstream . get( 'user end')

    #         #把句子交给NLP处理，生成文本块流
    #         nlp_dealer . addjob( sentence , StreamingOutput)
    #         tts_dealer . addjob( StreamingOutput , audio_player)
    #         Audio_player . addjob(audioinfo , outputwebsocket)


    # async def handle_websocket(websocket, path):
    #     main_dealing_textStream_to_AudioStream(websocket)

    # async def dealing_with_ws(nlp_dealer, audio_player):
    #     async with websockets.serve(handle_websocket, 'localhost', 8765):
    #         await asyncio.Future()  # keep server running

    async def test(self):
        
        from streamAudio2Text import startAudioInput
        import threading
        threading.Thread(target=startAudioInput, args=(self.dealchain,)).start()
        # import time
        # time.sleep(1)
        # self.dealchain.put('hello')
        # startAudioInput(self.dealchain)
        # await dealchain.running_loop()

    def run_forever(self):
        print('RUNNING FOREVER')
        import asyncio
        import time

        loop = asyncio.get_event_loop()
        loop.create_task(self.nlp_dealer.running_loop())
        loop.create_task(self.tts_dealer.running_loop())
        loop.create_task(self.audio_dealer.running_loop())
        loop.create_task(self.ui_dealer.running_loop())
        loop.create_task(self.dealchain.running_loop())
        loop.create_task(self.test())
        loop.run_forever()

if __name__ == "__main__":
    aicaller = AICaller()
    aicaller . run_forever()


# 后端实现的功能包括：
#     每次接受到一个连接（接收到连接信号）
#     创建一个类，包括
#         传入Audio的Stream
#         传出Audio的Stream
#         加入到一个轮询队列中

#     处理方法：
#         每次循环处理所有的


# 接收到连接后的处理
#   因为已经创立了一个In_audio
#   根据In_audio调用科大讯飞接口得到一个websocket
#   run_forever

# 客户端（硬件部分）
#     1、连接websocket，TCP确认连接成功
#     2、打开麦克风（以chunk的方式实现
#     3、每次读取一个chunk，发送到websocket，格式前后端统一


# 服务器端（跑在云上的）
#     启动5个dealer
#     ws_as : websocket to audiostream（接受到一个websocket，返回一个audiostream，异步执行的，
#         用于格式转化
#     asr_delaer : 通过流式读入的audiostream去转化textstream【(start ,None) ,  (mid , str) , (end , None)】
#     nlp_dealer : 把一个text,sentence 去转化textstream 最主要的部分
#         runing_forever():
#             得到一个任务 (add / cancel)
#             如果连接请求不超过100个
#                 启动一个异步的协程去运行这样一个sentence2textstream的过程，先查向量数据库，await，给openai去调用，得到一个request
#         add_job(text,textstream)
#         cancel_job(job)，通过一个索引找到这样一个任务，然后把整个协程停掉，用异常的方式
#     tts_dealer : 把一个textstream转化为audiostream
#         （不断读取textstream，如果）
    
#     启动websocket，监听
#     【每次监听到一个连接请求的时候，handle_websocket】



# 服务器
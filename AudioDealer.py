from queue import Queue
from JobAction import JobAction
#log
import logging
from Dealer import Dealer
from pygame import mixer
from TextStream import SigType
import asyncio
class AudioDealer(Dealer):
    # 只支持单机单个元素的输出目前是这样
    class JOB:
        def __init__(self, audioQueue):
            # get sentence and response textStream
            self.audioQueue = audioQueue
            self.statue = 'ACCEPTED'
            pass

        def cancel(self):
            logging.info('job.cancel')
            self.statue = 'CANCELLED'

    def __init__(self):
        super().__init__()
        self.lock = asyncio.Lock()
        mixer.init()
        pass

    def set_ui_dealer(self, ui_dealer):
        self.ui_dealer = ui_dealer

    async def main_deal_job(self, job : JOB):
        # logging.info('AUDIO main deal job')
        async with self.lock:
            audioQueue = job.audioQueue
            # logging.info('AUDIO deal job')
            import asyncio
            import io

            info = await audioQueue.get()
            # logging.info('deal job get info' + str(len(info)) + str(info))
            while info != SigType.END:
                text, audio_data = info
                # logging.info('deal job get audio data' + str(len(audio_data)))
                # print("time = ",time.time())
                await self.ui_dealer.add_job(self.ui_dealer.JOB('signal','speaking')) 
                await self.ui_dealer.add_job(self.ui_dealer.JOB('text',text)) 
                mixer.music.load(io.BytesIO(audio_data))
                mixer.music.set_volume(1)
                mixer.music.play()
                while mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                info = await audioQueue.get()
            await self.ui_dealer.add_job(self.ui_dealer.JOB('signal','waiting'))
            await self.ui_dealer.add_job(self.ui_dealer.JOB('text',''))
            logging.info('deal job end')

    async def deal_job(self, job : JOB):
        try:
            await self.main_deal_job(job)
        except:
            logging.info('deal job failed')
            pass
        
    
    async def clean(self):
        async with self.lock:
            mixer.quit()
            mixer.init()
        pass



if __name__ == '__main__':
    import asyncio
    import time
    import logging
    from TextStream import SigType
    from TextStream import TextStream
    
    async def test():
        from DealerChain import DealerChain
        dealerchain = DealerChain( nlp_dealer, tts_dealer , audio_dealer , ui_dealer)
        nlpjob , ttsjob , audiojob , textstream , audioQueue = await dealerchain.START('hello')
        while True:
            await asyncio.sleep(10)
            print ('7100s passed')
            await dealerchain . CLEAN(nlpjob,ttsjob,audiojob,textstream,audioQueue)
            nlpjob , ttsjob , audiojob , textstream , audioQueue = await dealerchain.START('what\'s wrong')

    logging.basicConfig(level=logging.INFO)
    from NLPDealer import NLPDealer
    from TTSDealer import TTSDealer
    from UIDealer import UIDealer
    nlp_dealer =  NLPDealer()
    tts_dealer = TTSDealer()
    audio_dealer = AudioDealer()
    ui_dealer = UIDealer()
    loop = asyncio.get_event_loop()
    loop.create_task(nlp_dealer.running_loop())
    loop.create_task(tts_dealer.running_loop())
    loop.create_task(audio_dealer.running_loop())
    loop.create_task(ui_dealer.running_loop())
    loop.create_task(test())
    loop.run_forever()

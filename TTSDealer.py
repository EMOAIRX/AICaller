from queue import Queue
import logging
from JobAction import JobAction
from Dealer import Dealer
class TTSDealer(Dealer):

    class JOB:
        def __init__(self, textStream , audioQueue):
            # get sentence and response textStream
            self.textStream = textStream
            self.audioQueue = audioQueue
            self.statue = 'ACCEPTED'
            pass

        def cancel(self):
            logging.info('job.cancel')
            self.statue = 'CANCELLED'

    def __init__(self):
        super().__init__()
        pass

    @staticmethod
    async def transform(InputText):
        from urllib import parse
        import requests #注意，request需要在monkey.patch_all()之后导入
        url = "https://dict.youdao.com/dictvoice?le=auto&audio=" + \
            parse.quote(InputText, encoding='utf-8')
        session = requests.Session()
        session.trust_env = False
        try:
            r = session.get(url)
            return r.content
        except:
            raise Exception("生成 MP3 文件出错")
        pass
    
    async def main_deal_job(self, job : JOB):
        import TextStream
        from TextStream import SigType
        textstream = job.textStream
        audioqueue = job.audioQueue
        import asyncio
        info = await textstream.get_sentence(wait=True, stop = SigType.DATA) 
        await asyncio.sleep(0.1)
        print('get info' , info)
        while info != SigType.END:
            text = info
            logging.info('get text ' + str(len(text)))
            audioinfo = await TTSDealer.transform(text)
            logging.info('get audioinfo ' + str(len(audioinfo)))
            await audioqueue.put( (text, audioinfo ) )
            info = await textstream.get_sentence(wait=True, stop = SigType.DATA)
            await asyncio.sleep(0.1)
        await audioqueue.put(SigType.END)

    async def deal_job(self, job : JOB):
        try:
            await self.main_deal_job(job)
        except:
            logging.info('deal job failed')
            pass
        

if __name__ == '__main__':
    import asyncio
    import time
    import logging
    from TextStream import SigType
    from TextStream import TextStream
    async def test():
        textstream = TextStream()
        audioQueue = asyncio.Queue()
        logging.info('test')
        await nlp_dealer.add_job( NLPDealer.JOB('hello' , textstream) )
        await tts_dealer.add_job( TTSDealer.JOB(textstream,audioQueue) )
        while True:
            t = await audioQueue.get()
            if t == SigType.END:
                break
            t,R = t
            print('get audioinfo', len(R))

    logging.basicConfig(level=logging.INFO)
    from NLPDealer import NLPDealer
    nlp_dealer =  NLPDealer()
    tts_dealer = TTSDealer()
    loop = asyncio.get_event_loop()
    loop.create_task(nlp_dealer.running_loop())
    loop.create_task(tts_dealer.running_loop())
    loop.create_task(test())
    loop.run_forever()

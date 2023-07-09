import asyncio
class DealerChain():
    
    def __init__(self , nlp_dealer , tts_dealer , audio_dealer , ui_dealer):
        self.nlp_dealer = nlp_dealer
        self.tts_dealer = tts_dealer
        self.audio_dealer = audio_dealer
        self.ui_dealer = ui_dealer
        self.audio_dealer.set_ui_dealer(ui_dealer)
        self.queue = asyncio.Queue( maxsize=5 )
        pass

    async def CLEAN(self,nlpjob,ttsjob,audiojob,textstream,audioQueue):
        await self.ui_dealer . add_job( self.ui_dealer.JOB('signal','listing') )
        await self.nlp_dealer . cancel_job(nlpjob)
        await self.tts_dealer . cancel_job(ttsjob)
        await self.audio_dealer . cancel_job(audiojob)
        await self.audio_dealer . clean()
        await textstream.clean()
        while not audioQueue.empty():
            await audioQueue.get()

    async def START(self,sentence):
        from TextStream import TextStream
        import asyncio
        import logging
        from NLPDealer import NLPDealer
        from TTSDealer import TTSDealer
        from AudioDealer import AudioDealer
        textstream = TextStream()
        audioQueue = asyncio.Queue()
        logging.info('START' + sentence)
        await self.ui_dealer . add_job( self.ui_dealer.JOB('signal','speaking') )
        await self.ui_dealer . add_job( self.ui_dealer.JOB('text',sentence) )
        nlpjob = NLPDealer.JOB(sentence , textstream)
        ttsjob = TTSDealer.JOB(textstream,audioQueue)
        audiojob = AudioDealer.JOB(audioQueue)
        await self.nlp_dealer.add_job( nlpjob )
        await self.tts_dealer.add_job( ttsjob )
        await self.audio_dealer.add_job( audiojob )
        return nlpjob , ttsjob , audiojob , textstream , audioQueue

    async def ONLY_SPEAK(self,settence):
        textstream = TextStream()
        audioQueue = asyncio.Queue()
        
    
    async def running_loop(self):
        print('dealer_chain . running loop')
        nlpjob,ttsjob,audiojob,textstream,audioQueue = None,None,None,None,None
        #多级需要维护多个这样的变量，用id来区分
        while True:
            print("TRYING TO GET INFO")
            result_text = await self.queue.get()
            print(result_text)
            if nlpjob != None:
                await self.CLEAN(nlpjob,ttsjob,audiojob,textstream,audioQueue)
            nlpjob , ttsjob , audiojob , textstream , audioQueue = await self.START(result_text)

    def put(self,result_text):
        print('dealer_chain.put' , result_text)
        self.queue.put_nowait(result_text)
        print("END PUT")
        print(self.queue.qsize())
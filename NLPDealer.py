from JobAction import JobAction
from SigType import SigType
#log
import logging
from Dealer import Dealer
class NLPDealer_direct(Dealer):
    class JOB:
        def __init__(self, sentence , textStream):
            # get sentence and response textStream
            self.sentence = sentence
            self.textStream = textStream
            self.statue = 'ACCEPTED'
            pass

        def cancel(self):
            self.textStream.put_sig( SigType.END )
            logging.info('job.cancel')
            self.statue = 'CANCELLED'

    def __init__(self):
        super().__init__()
        pass


    async def main_deal_job(self, job : JOB):
        logging.info('deal job')
        import asyncio
        import toolOpenai
        Success = False
        text = job.sentence
        textStream = job.textStream
        while not Success:
            try:
                #需要先调用一个向量数据
                response = toolOpenai.request(text , [])
                Success = True
                
            except:
                print('request failed')
                await asyncio.sleep(1)
        logging.info('deal job get response' + str(response))
        await textStream.put_sig( SigType.START )
        collect = ""
        for event in response:
            delta_words = event['choices'][0]['delta'].get("content", '')
            collect += delta_words
            # logging.info('deal job get delta_words' + str(delta_words))
            if len(collect) > 5:
                await textStream.put_str(collect)
                collect = ""
        if len(collect) > 0:
            await textStream.put_str(collect)
        await textStream.put_sig( SigType.END )
        
    async def deal_job(self, job : JOB):
        try:
            await self.main_deal_job(job)
        except:
            logging.info('deal job failed')
            pass


# class NLPDealer_lang(Dealer):
#     class JOB:
#         def __init__(self, sentence , textStream):
#             # get sentence and response textStream
#             self.sentence = sentence
#             self.textStream = textStream
#             self.statue = 'ACCEPTED'
#             pass

#         def cancel(self):
#             self.textStream.put_sig( SigType.END )
#             logging.info('job.cancel')
#             self.statue = 'CANCELLED'

#     def __init__(self):
#         super().__init__()
        
#         # 初始化DBchain实例
#         from langchainAI import initDBfromExternal
#         self.llm, self.qa_stuff = initDBfromExternal()

#         pass


#     async def main_deal_job(self, job : JOB, llm, qa_stuff):
#         logging.info('deal job')
#         import asyncio
#         import langchainAI
#         Success = False
#         text = job.sentence
#         textStream = job.textStream
#         while not Success:
#             try:
#                 #需要先调用一个向量数据
#                 await langchainAI.request(text , llm,  qa_stuff)
#                 Success = True
#             except:
#                 print('request failed')
#                 await asyncio.sleep(1)
#         print('end langchainAI.request')
#         handler = llm.callbacks[0]
#         print('handle = ' , handler)

#         logging.info('deal job get response')
#         await textStream.put_sig( SigType.START )
#         collect = ""
#         while True:
#             token = handler.queue.get()
#             if token == SigType.END:
#                 # All tokens have been generated
#                 break
#             collect += token
#             if len(collect) > 5:
#                 await textStream.put_str(collect)
#                 collect = ""
#         if len(collect) > 0:
#             await textStream.put_str(collect)
#         await textStream.put_sig( SigType.END )

        
#     async def deal_job(self, job : JOB):
#         try:
#             await self.main_deal_job(job, self.llm, self.qa_stuff)
#         except:
#             logging.info('deal job failed')
#             # clean self.llm.callbacks[0].queue()
#             while self.llm.callbacks[0].queue.empty() == False:
#                 self.llm.callbacks[0].queue.get()
#             pass
        

class NLPDealer(NLPDealer_direct):
    pass

if __name__ == '__main__':
    import asyncio
    import time
    import logging
    from TextStream import TextStream
    async def test():
        textstream = TextStream()
        logging.info('test')
        await dealer.add_job( dealer.JOB('hello' , textstream) )
        logging.info('test')
        while True:
            res = await textstream.get_sentence(wait=True, stop = SigType.DATA) 
            if res == None:
                break
            print(res)
    logging.basicConfig(level=logging.INFO)
    dealer = NLPDealer()
    loop = asyncio.get_event_loop()
    loop.create_task(dealer.running_loop())
    loop.create_task(test())
    loop.run_forever()

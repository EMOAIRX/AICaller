



# class ASRDealer:

#     class JOB:
#         def __init__(self, websocket , textStream):
#             self.websocket = websocket
#             self.textStream = textStream

#     def running_loop(self):
#         pass 

#     def add_job(self, job):
#         # websockets to text job
#         #get info from job.websockets and transform it into a TextStream
#         pass



# class NLPDealer:

#     from enum import Enum

#     class JobAction(Enum):
#         ADDJOB = 1
#         CANCELJOB = 2

#     class JOB:
#         def __init__(self, sentence , textStream):
#             # get sentence and response textStream
#             self.sentence = sentence
#             self.textStream = textStream
#             self.statue = 'ACCEPTED'
#             pass

#         def set_statue(self, statue):
#             self.statue = statue

#         def cancel(self):
#             self.statue = 'CANCELLED'

#     def __init__(self):
#         from queue import Queue
#         self.queue = Queue()
#         pass

#     async def deal_job(self, job):
#         import toolOpenai
#         import openai
#         Success = False
#         text = job.sentence
#         textStream = job.textStream
#         while not Success:
#             try:
#                 #需要先调用一个向量数据
#                 response = toolOpenai.request(text , [])
#                 Success = True
#             except:
#                 print('request failed')
#                 asyncio.sleep(1)
#         for event in response: #没有的话会切换，可以调度。
#             await textStream.put(
#                     event['data']['text']... 
#                 )
#         pass

#     async def running_loop(self): #放在loop里面的，所以一个async
#         import asyncio
#         tasks = []
#         while True:
#             head = await self.queue.get( block = True )
#             if head[0] == self.JobAction.ADDJOB:
#                 while len(tasks) >= 100:
#                     await asyncio.wait(tasks)
#                     tasks = [task for task in tasks if not task.done()]
#                 assert len(tasks) < 100
#                 tasks.append( (head[0] , asyncio.create_task(self.deal_job(head[1]))) )
#             elif head[0] == self.JobAction.CANCELJOB:
#                 for task in tasks:
#                     if task[1].job == head[1]:
#                         task[1].cancel()
#                         break

#     def add_job(self, job):
#         self.queue.put((self.JobAction.ADDJOB,job))
#         pass

#     def cancel_job(self, job):
#         self.queue.put((self.JobAction.CANCELJOB,job))
#         pass


# class TTSDealer:
#     class JOB:
#         def __init__(self, textStream , audioStream):
#             pass

#     def __init__(self):
#         pass
        
#     def add_job(self, job):
#         # get info from job.textStream and for each sentence in it, transform it into AudioStream
#         pass


# class AudioPlayer:
#     class JOB:
#         def __init__(self, audioStream , websocket):
#             # input audioStream and puts to websocket
#             pass

#     def __init__(self):
#         pass

#     def add_job(self, job):
#         #get info from job.audioStream and transform it into a TextStream
#         pass

# # 如何打断?
# # 当我知道这句话还在处理的时候，我要终止之后的NLP_dealer的处理，终止TTSDelaer的处理，终止AudioPlayer的处理。
# # 把 job 的状态设置成 INTERRUPTED
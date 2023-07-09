import asyncio
import logging
from JobAction import JobAction
class Dealer():
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.LIMIT = 10
        pass

    async def deal_job(self, job):
        # Add default behavior here
        pass
    
    @staticmethod
    def DONE_CALLBACK(future):
        logging.info('future done')
        if future.exception() != None:
            logging.info('future exception')
            logging.info(future.exception())
            logging.info(future)
            return
        if future.cancelled():
            print(future.result())
            print(future)
            # future.job.cancel()
            logging.info('future cancelled')
            return
        logging.info('future not cancelled')
        
    
    async def running_loop(self): #放在loop里面的，所以一个async
        logging.info('running loop')
        import asyncio
        tasks = []
        while True:
            logging.info('get head')
            head = None
            while head == None:
                while self.queue.empty():
                    await asyncio.sleep(0.01)
                head = await self.queue.get()

            logging.info('get head' + str(head) )
            if head[0] == JobAction.ADDJOB:
                tasks = [task for task in tasks if not task[1].done()]
                while len(tasks) >= self.LIMIT: #这地方有bug，现在可能没了吧
                    logging.info('asyncio wait in Runing Loop in Dealer')
                    await asyncio.wait ( [task[1] for task in tasks if not task[1].done()] )
                    tasks = [task for task in tasks if not task[1].done()]
                assert len(tasks) < self.LIMIT
                task = (head[1] , asyncio.create_task(self.deal_job(head[1])))
                tasks.append( task )
                task[1].add_done_callback(self.DONE_CALLBACK)

            elif head[0] == JobAction.CANCELJOB:
                tasks = [task for task in tasks if not task[1].done()]
                for task in tasks:
                    if task[0] == head[1]:
                        print('CANCEL_JOB!')
                        task[1].cancel()
                        break

    async def add_job(self, job):
        logging.info('add job')
        await self.queue.put( (JobAction.ADDJOB,job) )

    async def cancel_job(self, job):
        logging.info('cancel job')
        await self.queue.put((JobAction.CANCELJOB,job))

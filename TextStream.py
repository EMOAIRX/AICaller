
import asyncio
from SigType import SigType

class TextStream:
    def __init__(self):
        self.Lock = asyncio.Lock()
        self.infoList = []
        self.collected = ""
        self.count = {}
        self.count[SigType.END] = 0
        self.count[SigType.DATA] = 0



    async def put_sig(self , sig):
        import logging
        logging.info('put sig' + str(sig))
        print(self.infoList)
        async with self.Lock:
            # logging.info('real put sig' + str(sig))
            if sig == SigType.START:
                self.collected = ""
            if sig == SigType.END:
                if len(self.collected) > 0:
                    self.infoList += [(SigType.DATA , self.collected)] 
                    self.collected = ""
                    self.count[ SigType.DATA ] += 1
                self.infoList += [(SigType.END , None)]     
                self.count [ SigType.END ] += 1

    async def put_str(self , TextBlock):
        import logging
        import asyncio
        logging.info('put str' + TextBlock)
        async with self.Lock:
            self.collected += TextBlock
            SPLIT = ",.!?;:，。！？；："
            last_exist = max (self.collected.rfind( x ) for x in SPLIT)
            if last_exist == -1:
                pass
            else:
                parts = [self.collected[:last_exist + 1] , self.collected[last_exist + 1:]]
                self.infoList += [(SigType.DATA , parts[0])]
                self.collected = parts[1]
                self.count[ SigType.DATA ] += 1
                await asyncio.sleep(0.01)#是否可以用yield取代？
            # print(self.infoList, self.collected)


    async def clean(self):
        async with self.Lock:
            self.infoList = []
            self.collected = ""
            self.count = {}
            self.count[SigType.END] = 0
            self.count[SigType.DATA] = 0

    # async def get_sentence(self , wait = True , stop = SigType.DATA) -> str | None | SigType:
    async def get_sentence(self , wait = True , stop = SigType.DATA):
        import logging
        logging.info('get sentence')
        if wait == False:
            await self.Lock.acquire()
            if self.count[stop]:
                self.Lock.release()
                return None
        else:
            await self.Lock.acquire()
            while self.count[stop] == 0 and self.count[SigType.END] == 0:
                self.Lock.release()
                await asyncio.sleep(0.01)
                await self.Lock.acquire()
        logging.info('get sentence get lock' + str(self.count[SigType.DATA]) + str(self.count[SigType.END]))
        if stop == SigType.DATA:
            if self.infoList[0][0] == SigType.END:
                self.infoList.pop(0)
                self.count [ SigType.END ] -= 1
                self.Lock.release()
                return SigType.END
                
            collected = self.infoList.pop(0)[1]
            self.count [ SigType.DATA ] -= 1
            while len(self.infoList)>0 and (self.infoList[0][0] != SigType.END):
                collected += self.infoList.pop(0)[1]
                self.count [ SigType.DATA ] -= 1
            output = collected
            self.Lock.release()
            return output
        elif stop == SigType.END:
            collected = ""
            while self.infoList[0][0] != SigType.END:
                self.count [ SigType.DATA ] -= 1
                collected += self.infoList.pop(0)[1] 
            self.count [ SigType.END ] -= 1
            self.infoList.pop(0)
            output = collected
            self.Lock.release()
            return output


        return None
import os

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file

# 将OpenAI API密钥保存在环境变量中
os.environ['OPENAI_API_KEY'] = '....'
from keys import openai_APIKEY , openai_BASE


from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DataFrameLoader
from typing import Any
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferWindowMemory

# index = VectorstoreIndexCreator(
#     vectorstore_cls=DocArrayInMemorySearch
# ).from_loaders([loader])

##Prompt Engineering
from langchain import PromptTemplate

template_string = """
<ctx>
{context}
</ctx>
------
<hs>
{history}
</hs>
------
{question}
"""
prompt_template = PromptTemplate(
    input_variables=["history", "context", "question"],
    template=template_string,
)

import threading
import queue

class MyCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue.Queue()

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.queue.put(token)


def initDB(csvFile, embeddings, llm, chain_type, window_size=5):

    loader = CSVLoader(file_path=csvFile , encoding='utf-8')
    docs = loader.load()       

    db = DocArrayInMemorySearch.from_documents(
        docs, 
        embeddings
    )

    retriever = db.as_retriever()
    qa_stuff = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type=chain_type, 
        retriever=retriever, 
        verbose=False,
            chain_type_kwargs={
                "verbose": False,
                "prompt": prompt_template,
                "memory": ConversationBufferWindowMemory(
                    k=window_size,
                    memory_key="history",
                    input_key="question"),
                }
        
    )

    return llm, qa_stuff

def initDBfromExternal():
    file = 'products.csv' #需要补充
    embeddings = OpenAIEmbeddings(
            client = "text-embedding-ada-002",
            # openai_api_key=openai_APIKEY,
            # openai_api_base=
        )

    handler = MyCallbackHandler()
    llm = ChatOpenAI(
            streaming=True, callbacks=[handler], temperature=0.2,
            openai_api_key=openai_APIKEY,
            openai_api_base=openai_BASE,
            client="gpt-3.5-turbo",
        )

    llm, qa_stuff = initDB(file, embeddings, llm, "stuff", window_size=5)  # Unpack the returned values
    return llm, qa_stuff 

# def request_locol(query, llm, qa_stuff):
#     handler = llm.callbacks[0]  # 
 

#     def print_tokens():
#         while True:
#             token = handler.queue.get()
#             print(token, end='', flush=True)

#     # Start a new thread to print tokens
#     threading.Thread(target=print_tokens).start()
#     qa_stuff.run(query)

async def request(query, llm, qa_stuff):
    print('request  , query = ' , query)
    import asyncio
    from SigType import SigType
    handler = llm.callbacks[0]
    def run(query):
        qa_stuff.run(query)
        handler.queue.put(SigType.END)
    threading.Thread(target=run, args=(query,)).start()
    print('END REQ')





if __name__ == "__main__":

    # file = 'products.csv'
    # embeddings = OpenAIEmbeddings()

    # llm = ChatOpenAI(streaming=True, callbacks=[MyCallbackHandler()], temperature=0.2)

    # llm, qa_stuff = initDB(file, embeddings, llm, "stuff", window_size=5)

    llm, qa_stuff = initDBfromExternal()

    # Start a new thread to print tokens
    # threading.Thread(target=print_tokens, args=(handler,)).start()

    while True:
        query = input("请输入您的问题：")
        # request_locol(query,llm, qa_stuff)
        # response = qa_stuff.run(query)
        # print('\n')



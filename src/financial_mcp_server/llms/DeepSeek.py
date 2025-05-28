import os
from typing import List
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import  DashScopeEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()


def DeepSeekV3():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.environ.get("DEEPSEEK_API_KEY"),  # 自行搞定  你的秘钥
        base_url="https://api.deepseek.com"
    )
def DeepSeekR1():
    return ChatOpenAI(
        model="deepseek-reasoner",
        api_key=os.environ.get("DEEPSEEK_API_KEY"),  # 自行搞定  你的秘钥
        base_url="https://api.deepseek.com"
    )
def TongyiEmbedding()->DashScopeEmbeddings:
    api_key=os.environ.get("DASHSCOPE_API_KEY")
    return DashScopeEmbeddings(dashscope_api_key=api_key,
                           model="text-embedding-v1")

def QdrantVecStoreFromDocs(docs:List[Document]):
    eb=TongyiEmbedding()
    return QdrantVectorStore.from_documents(docs,eb,url="http://localhost:6333")

def QdrantVecStore(eb:DashScopeEmbeddings,collection_name:str):
    return  QdrantVectorStore.\
        from_existing_collection(embedding=eb,
         url="http://localhost:6333",
          collection_name=collection_name)


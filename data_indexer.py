
from docarray import BaseDoc
from docarray.typing import  NdArray
from docarray import DocList
import numpy as np
from vectordb import InMemoryExactNNVectorDB, HNSWVectorDB

from web import generate_embedding


class MiniLMDoc(BaseDoc):
    text:str = ''
    embedding:NdArray[384]


def index_data(sentence, embedding):
    #Specify your workspace path
    db = HNSWVectorDB[MiniLMDoc](workspace="./vdb_local_store")

    # need_index = False
    need_index = True
    if need_index:
        #Index a list of ducuments with random embeddings
        doc_list = [MiniLMDoc(text=sentence,embedding=embedding)]
        return db.index(inputs=DocList[MiniLMDoc](doc_list))


def get_top_n_match_item(sentence, embedding, limit):
    try:
        db = HNSWVectorDB[MiniLMDoc](workspace="./vdb_local_store")
        query = MiniLMDoc(text=sentence, embedding= embedding)
        results = db.search(inputs=DocList[MiniLMDoc]([query]), limit=limit)
        if len(results)> 0:
            return  results[0]
    except Exception as e:
        print("error:", e)
        return None


def check_data_exist(sentence, embedding):
    try:
        db = HNSWVectorDB[MiniLMDoc](workspace="./vdb_local_store")
        query = MiniLMDoc(text=sentence, embedding= embedding)
        results = db.search(inputs=DocList[MiniLMDoc]([query]), limit=limit)
        if len(results)> 0:
            return True
        return False
    except Exception as e:
        print("error:", e)
        return None


if __name__ == "__main__":
    text = "hello please generate embedding now, take this sentense as input"
    embedding = generate_embedding(text)
    print(index_data(text,embedding))
    print(check_data_exist(text,embedding))
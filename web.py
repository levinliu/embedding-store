import json
import os

import gradio as gr
from sentence_transformers import SentenceTransformer

import numpy as np


def greet(name):
    return "Hello " + name + "!"


# fix issue : TypeError: Object of type ndarray is not JSON serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def generate_embedding(sentences):
    local_model_path = "D:/PycharmProjects/embedding_store/models/all-MiniLM-L6-v2"
    if 'LEVIN_TECH_MODEL_PATH' in os.environ:
        local_model_path = os.environ['LEVIN_TECH_MODEL_PATH']
    # model = SentenceTransformer('sentence_transformers/all-MiniLM-L6-v2')
    model = SentenceTransformer(local_model_path)
    print(f'encoding - {sentences}')
    return model.encode(sentences=sentences)


if __name__ == '__main__':
    print(generate_embedding('test generation'))
    demo = gr.Interface(fn=generate_embedding, inputs="text", outputs="text")
    demo.launch()

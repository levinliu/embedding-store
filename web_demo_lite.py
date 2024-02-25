import numpy as np
import gradio as gr
import sys
import os
from web import generate_embedding



class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def isatty(self):
        return False


def sys_redirect_stdout(log_file_path):
    os.environ['LEVIN_TECH_GRADIO_APP_LOG'] = log_file_path
    print(f"redirected log to path - {log_file_path}")
    sys.stdout = Logger(log_file_path)


def redirect_stdout():
    sys_redirect_stdout('./app.log')


def read_logs():
    sys.stdout.flush()
    xlog = os.environ['LEVIN_TECH_GRADIO_APP_LOG']
    with open(xlog, "r") as f:
        return f.read()


def index_data(a,b):
    pass

def get_top_n_match_item(a,b,c):
    pass

def generate_and_index_data(sentense):
    embedding = generate_embedding(sentense)
    print(index_data(sentense, embedding))
    return "save embedding : " + str(embedding)


def lookup(sentense, limit=3):
    embedding = generate_embedding(sentense)
    result_data = get_top_n_match_item(sentense, embedding, int(limit))
    print('result_data::', result_data)
    tdata = []
    if result_data is None:
        return tdata
    # for i in range(5):
    #     tdata.append(['a', 'b', 1 * i])

    for i in range(len(result_data.matches)):
        # tdata.scores:
        match = result_data.matches[i]
        score = result_data.scores[i]
        tdata.append([score, match.text, str(match.embedding)])
    print("finish query")
    return tdata


with gr.Blocks(title="AIEditor") as demo:
    gr.Markdown("AIEditor")
    with gr.Tab("CodeGenerator"):
        sent_in = gr.TextArea(label="Your queries")
        emb_out = gr.Textbox(label="Answer")
        proc_btn = gr.Button(label="Process")


    proc_btn.click(generate_and_index_data, inputs=sent_in, outputs=emb_out)

print("starting the gradio app")
import os

port = int(os.environ['LEVIN_TECH_APP_PORT']) if 'LEVIN_TECH_APP_PORT' in os.environ else 7086

sys_redirect_stdout(os.path.join(os.getcwd(),'app.log'))

demo.launch(server_port=port, server_name="0.0.0.0")

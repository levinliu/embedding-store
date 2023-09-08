import numpy as np
import gradio as gr

from data_indexer import index_data, get_top_n_match_item
from web import generate_embedding


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


with gr.Blocks(title="EmbeddingStore") as demo:
    gr.Markdown("EmbeddingStore")
    with gr.Tab("SentenceToEmbedding"):
        sent_in = gr.Textbox(label="Input Sentence")
        emb_out = gr.Textbox(label="Embedding")
        proc_btn = gr.Button(label="Process")

    with gr.Tab("Search text Image"):
        with gr.Row():
            keyword_input = gr.Textbox(label="Input sample text to query")
        with gr.Row():
            limit_input = gr.Textbox(label="Limit", value=3)

        with gr.Row():
            image_output = gr.DataFrame(headers=["Score", "Text", "Embedding"],
                                        datatype=["str", "str", "number"])
        with gr.Row():
            image_button = gr.Button("Lookup")

    proc_btn.click(generate_and_index_data, inputs=sent_in, outputs=emb_out)
    image_button.click(lookup, inputs=[keyword_input, limit_input], outputs=image_output)

print("starting the gradio app")
demo.launch()

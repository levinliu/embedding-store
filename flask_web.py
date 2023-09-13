
import gradio as gr
from flask import Flask, render_template, request

app = Flask(__name__)

def greet(name):
    return "Hello, " + name + "!"

iface = gr.Interface(fn=greet, inputs="text", outputs="text")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/greet", methods=["POST","GET"])
def api():
    data = request.get_json(force=True)
    name = data["name"]
    return {"result": iface.process([name])[0]}







if __name__ == "__main__":
    app.run()


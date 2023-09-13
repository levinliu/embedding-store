import os
import sys


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


if __name__ == "__main__":
    import gradio as gr

    with gr.Blocks() as demo:
        with gr.Row():
            input = gr.Textbox(label="input", placeholder="type something here")
            output = gr.Textbox(label="output")
        btn = gr.Button("Run")


        def process(x):
            print(f"start processing for {x}")
            return f'processed {x}'


        btn.click(process, input, output)

        print("hello gradio log test")
        logs = gr.Textbox(label="runtime log")
        demo.load(read_logs, None, logs, every=1)

    redirect_stdout()
    demo.queue().launch()

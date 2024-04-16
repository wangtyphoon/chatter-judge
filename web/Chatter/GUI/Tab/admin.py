import gradio as gr
from Chatter.Database.models import add_question

def init_admin_tab(*args, **kwargs):
    with gr.Row():
        gr.Interface(
            fn=add_question,
            inputs=[
            gr.Textbox(label="題目名稱"),
            gr.Textbox(label="題目描述"),
            gr.Textbox(label="Scope"),
            gr.Textbox(label="輸入"),
            gr.Textbox(label="輸出"),
            ],
            outputs="text",
            )
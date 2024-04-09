# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import gradio as gr

from Chatter.Utils.Update import get_question_description


def submit_background_listener(
    selected_scope_name: gr.Dropdown,
    selected_question_name: gr.Dropdown,
    output_block: gr.Markdown,
):
    selected_question_name.change(
        fn=get_question_description,
        inputs=[
            selected_scope_name,
            selected_question_name,
        ],
        outputs=output_block,
    )
    selected_scope_name.change(
        fn=get_question_description,
        inputs=[
            selected_scope_name,
            selected_question_name,
        ],
        outputs=output_block,
    )

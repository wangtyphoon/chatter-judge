# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

from typing import Any

import gradio as gr

from Chatter.GUI.Information import Header as heaader
from Chatter.GUI.Login import Auth as auth
from Chatter.GUI.Tab import History as history
from Chatter.GUI.Tab import Submit as submit


def build_chatter_judge(
    *args: Any,
    **kwargs: Any,
) -> gr.Blocks:
    demo = gr.Blocks(
        title="Chatter Judge",
    )

    with demo:
        gr.Markdown(heaader.ee_judge_header)

        submit_tab = submit.init_submit_tab()
        history_tab = history.init_history_tab()

        with gr.Tab("Race Bar"):
            gr.Markdown(heaader.race_bar_page_header)

        with gr.Tab("Judge Mechanism"):
            gr.Markdown(heaader.judge_mechanism_page_header)

        with gr.Tab("Judge Developers"):
            gr.Markdown(heaader.judger_developer_page_header)

    # demo.auth=auth.auth_admin             # temporary disable auth
    # demo.auth_message = 'Welcome to Chatter Judge!!!'

    return demo


def build_admin_management(
    *args: Any,
    **kwargs: Any,
) -> gr.Blocks:
    admin = gr.Blocks(
        title="Chatter Admin",
    )

    with admin:
        gr.Markdown(
            """
# Chatter Admin

Welcome to Chatter Admin! This is the admin page for Chatter Judge.
"""
        )

    return admin


def build_home_page() -> gr.Blocks:
    home = gr.Blocks(
        title="Chatter Home",
    )

    with home:
        gr.Markdown(
            """
# Chatter Home

Welcome to Chatter Home! This is the home page for Chatter Judge.

[Chatter Judge](/judge/) | [Chatter Admin](/admin/)
"""
        )

        with gr.Tab("Login"):
            gr.Markdown(
                """
# Login

Welcome to Chatter Login! This is the login page for Chatter Judge.
"""
            )

            with gr.Row():
                with gr.Column():
                    gr.Label("Username")
                    username = gr.Textbox()
                with gr.Column():
                    gr.Label("Password")
                    password = gr.Textbox()

                btn = gr.Button("Login")
                # TODO: Redirect with js
                btn.click(fn=auth.login, inputs=[username, password])

        with gr.Tab("Register"):
            gr.Markdown(
                """
# Register

Welcome to Chatter Register! This is the register page for Chatter Judge.

WIP
"""
            )

    return home

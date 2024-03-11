# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

from typing import Any

import gradio as gr

from Chatter.GUI.Information import Header as heaader
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
# Admin Panel

Welcome, admin! This is the admin page for Chatter Judge.

WIP
"""
        )

    return admin


def build_home_page() -> gr.Blocks:
    with gr.Blocks(title="Chatter Home") as home:
        # FIXME: Is really annoying that the link above will force the user to open a new tab...
        gr.Markdown(
            """
# Chatter Home

Welcome! This is the home page for Chatter Judge.

[Judge](/judge/) | [Admin Panel](/admin/)
"""
        )

        with gr.Tab("Login"):
            gr.Markdown(
                """
# Login

Welcome! This is the login page for Chatter Judge.
"""
            )

            with gr.Row():
                gr.Textbox(label="Username", elem_id="username", interactive=True)
                gr.Textbox(label="Password", elem_id="password", type="password", interactive=True)

                gr.Button("Login", elem_id="login", interactive=True)

        with gr.Tab("Register"):
            gr.Markdown(
                """
# Register

Welcome! This is the register page for Chatter Judge. (WIP)
"""
            )
            with gr.Row():
                gr.Textbox(label="Username", elem_id="username", interactive=True)
                gr.Textbox(label="Password", elem_id="password", type="password", interactive=True)

                gr.Button("Login", elem_id="login", interactive=True)

        # TODO: Put this ugly js hack into a separate file
        home.load(
            _js="""\
params=new URLSearchParams(window.location.search),params.get("error")&&alert(params.get("error")),document.getElementById("login").onclick=(()=>{const e=document.createElement("form");let a=document.createElement("input");a.name="username",a.value=document.querySelector("#username > label > textarea").value,e.appendChild(a),(a=document.createElement("input")).name="password",a.value=document.querySelector("#password > label > input").value,e.appendChild(a),e.method="POST",e.action="/auth/login",e.style.display="none",document.body.appendChild(e),e.submit()}),()=>{}
""".strip()
        )

    return home

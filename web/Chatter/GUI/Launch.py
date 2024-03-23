# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

from typing import Any

import gradio as gr

from Chatter.GUI.Information import Header as header  # 標題資訊
from Chatter.GUI.Tab import History as history  # 歷史記錄頁面
from Chatter.GUI.Tab import Submit as submit  # 提交頁面


def build_chatter_judge(*args: Any, **kwargs: Any) -> gr.Blocks:
    """構建 Chatter Judge 頁面"""

    demo = gr.Blocks(title="Chatter Judge")  # 頁面標題

    with demo:
        gr.Markdown(header.ee_judge_header)  # 顯示 EE Judge 標題

        # 初始化提交和歷史記錄頁面
        submit_tab = submit.init_submit_tab()
        history_tab = history.init_history_tab()

        # 使用 Tab 顯示不同頁面
        with gr.Tab("Race Bar"):
            gr.Markdown(header.race_bar_page_header)  # 顯示競賽列頁面標題
        with gr.Tab("Judge Mechanism"):
            gr.Markdown(header.judge_mechanism_page_header)  # 顯示評判機制頁面標題
        with gr.Tab("Judge Developers"):
            gr.Markdown(header.judger_developer_page_header)  # 顯示評判開發者頁面標題

    # 暫時禁用身份驗證
    # demo.auth = auth.auth_admin
    # demo.auth_message = 'Welcome to Chatter Judge!!!'

    return demo


def build_admin_management(*args: Any, **kwargs: Any) -> gr.Blocks:
    """構建管理面板頁面"""

    admin = gr.Blocks(title="Chatter Admin")  # 頁面標題

    with admin:
        gr.Markdown(
            """# Admin Panel
Welcome, admin! This is the admin page for Chatter Judge.
WIP"""  # 保持英文
        )  # 顯示管理面板標題和說明

    return admin


def build_home_page() -> gr.Blocks:
    """構建首頁"""

    with gr.Blocks(title="Chatter Home") as home:  # 頁面標題
        # FIXME: Is really annoying that the link above will force the user to open a new tab...
        gr.Markdown(
            """# Chatter Home
Welcome! This is the home page for Chatter Judge.
[Judge](/judge/) | [Admin Panel](/admin/)"""  # 保持英文
        )  # 顯示首頁標題和連結

        # 登錄頁面
        with gr.Tab("Login"):
            gr.Markdown(
                """# Login
Welcome! This is the login page for Chatter Judge."""  # 保持英文
            )  # 顯示登錄頁面標題
            with gr.Row(elem_id="login-row"):
                # 用户名和密码输入框
                gr.Textbox(label="Username", elem_id="username", interactive=True)
                gr.Textbox(label="Password", elem_id="password", type="password", interactive=True)
                gr.Button("Login", elem_id="login", interactive=True)  # 登錄按钮

        # 註冊頁面
        with gr.Tab("Register"):
            gr.Markdown(
                """# Register
Welcome! This is the register page for Chatter Judge. (WIP)"""  # 保持英文
            )  # 顯示註冊頁面標題
            with gr.Row(elem_id="register-row"):
                # 用户名和密码输入框
                gr.Textbox(label="Username", elem_id="username", interactive=True)
                gr.Textbox(label="Password", elem_id="password", type="password", interactive=True)
                gr.Button("register", elem_id="register", interactive=True)  # 登錄按钮

        # TODO: Put this ugly js hack into a separate file
        home.load(
            _js="""\
params=new URLSearchParams(window.location.search),
params.get("msg")&&alert(params.get("msg")),
document.getElementById("login").onclick=(()=>{
    const e=document.createElement("form");
    let a=document.createElement("input");
    a.name="username",
    a.value=document.querySelector("#login-row > div > #username > label > textarea").value,
    e.appendChild(a),
    (a=document.createElement("input")).name="password",
    a.value=document.querySelector("#login-row > div > #password > label > input").value,
    e.appendChild(a),
    e.method="POST",
    e.action="/auth/login",
    e.style.display="none",
    document.body.appendChild(e),
    e.submit()
}),
document.getElementById("register").onclick=(()=>{
    const e=document.createElement("form");
    let a=document.createElement("input");
    a.name="username",
    a.value=document.querySelector("#register-row > div > #username > label > textarea").value,
    e.appendChild(a),
    (a=document.createElement("input")).name="password",
    a.value=document.querySelector("#register-row > div > #password > label > input").value,
    e.appendChild(a),
    e.method="POST",
    e.action="/auth/register",
    e.style.display="none",
    document.body.appendChild(e),
    e.submit()
}),
()=>{}""".strip()
        )  # 加载 JS 代码处理登录逻辑

    return home

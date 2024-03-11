# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os

import gradio as gr
from fastapi import FastAPI

from Chatter.GUI.Launch import (build_admin_management, build_chatter_judge,
                                build_home_page)

FAVICON_PATH = os.path.join(".", "static", "favicon.ico")
JUDGE_PATH = "/judge/"
ADMIN_PATH = "/admin/"


def build_and_mount_playground(app: FastAPI) -> FastAPI:
    playground = build_chatter_judge()
    playground.favicon_path = FAVICON_PATH

    app = gr.mount_gradio_app(app, playground, path=JUDGE_PATH)

    playground = build_admin_management()
    playground.favicon_path = FAVICON_PATH
    app = gr.mount_gradio_app(app, playground, path=ADMIN_PATH)

    playground = build_home_page()
    playground.favicon_path = FAVICON_PATH
    app = gr.mount_gradio_app(app, playground, path="/")

    return app

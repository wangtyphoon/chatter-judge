# -*- coding: utf-8 -*-
"""
Create Date: 2024/01/07
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import gradio as gr


def login(username: str, password: str, request: gr.Request) -> str | None:
    req = request.request  # need to use fastapi.Request to access session
    # TODO: Query the database to check the username and password
    print(req.session)
    req.session["user"] = username
    print(req.session)
    return username

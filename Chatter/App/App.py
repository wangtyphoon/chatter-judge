# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os
import secrets

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from Chatter.Utils.Build import ADMIN_PATH, JUDGE_PATH, build_and_mount_playground

app = FastAPI(
    title="Chatter Judge",
    description="Judge with ChatGPT",
    version="Chatter-v0.0.1-beta",
    docs_url="/docs",
)
os.makedirs("static", exist_ok=True)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
app = build_and_mount_playground(app)


@app.middleware("http")
async def check_auth(request: Request, call_next):
    if request.url.path.startswith(ADMIN_PATH):
        if request.session.get("user") != "admin":
            return JSONResponse(status_code=403, content={"message": "Not authenticated"})
    elif request.url.path.startswith(JUDGE_PATH):
        if not request.session.get("user"):
            return JSONResponse(status_code=403, content={"message": "Not authenticated"})

    return await call_next(request)


app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(
        "./static/favicon.ico",
    )

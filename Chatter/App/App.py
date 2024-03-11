# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os
import secrets
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from Chatter.Utils.Build import (ADMIN_PATH, JUDGE_PATH,
                                 build_and_mount_playground)

AUTH_NEEDED_PATH = [ADMIN_PATH, JUDGE_PATH]

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


@app.post("/auth/login")
async def login(
    username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request
) -> RedirectResponse:
    # TODO: Use database
    if username == "admin" and password == "admin":
        request.session["user"] = username
        return RedirectResponse(url=ADMIN_PATH, status_code=303)
    elif username == "user" and password == "user":
        request.session["user"] = username
        return RedirectResponse(url=JUDGE_PATH, status_code=303)
    else:
        return RedirectResponse(url=f"/?error=Invalid username or password", status_code=303)


@app.get("/auth/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


app = build_and_mount_playground(app)


@app.middleware("http")
async def check_auth(request: Request, call_next):
    current_user = request.session.get("user")
    if not current_user and any(request.url.path.startswith(path) for path in AUTH_NEEDED_PATH):
        return RedirectResponse(url="/", status_code=303)

    if request.url.path.startswith(ADMIN_PATH) and current_user != "admin":
        return JSONResponse(status_code=403, content={"message": "Not authorized"})

    return await call_next(request)


app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(
        "./static/favicon.ico",
    )

# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os
from enum import Enum

import httpx

SANDBOX_URL = os.environ["SANDBOX_URL"]


class Result(str, Enum):
    SUCCESS = "success"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEED = "time_limit_exceed"


def execute_code(code, selected_homework_name, selected_question_name, *args, **kwargs):
    with httpx.Client(base_url=SANDBOX_URL) as client:
        r = client.post(
            "/",
            json={
                "code": code,
                "input": "a",
            },
        )
        if r.status_code != 200:
            return "### Unknown error"
        result = r.json()
        print(result)
        status = Result(result["status"])
        msg = result["msg"]
        if status == Result.SUCCESS:
            # TODO: Handle the message
            msg = bytes.fromhex(msg)
            if msg == b"Hello World\n":
                return "### Your code results: AC"
            return f"### Your code results: WA"
        elif status == Result.RUNTIME_ERROR:
            # TODO: Maybe need to escape the message before rendering
            return f"### Your code results: {result['status']}\n{bytes.fromhex(msg)}"

        return f"### Your code results: {result['status']}"

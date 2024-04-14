# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import os
from enum import Enum

import httpx
from sqlalchemy import select

from Chatter.ChatBot.finetune import code_advice
from Chatter.Database.connection import get_db
from Chatter.Database.models import InputAndOutput, Question

TIMEOUT = 15
SANDBOX_URL = os.environ["SANDBOX_URL"]


class Result(str, Enum):
    SUCCESS = "success"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEED = "time_limit_exceed"


async def execute_code(code: str, scope: str, question_name: str):
    if not code:
        raise ValueError("Code is empty")
    if len(code) > 5000:
        # XXX: Is this a good limit?
        raise ValueError("Code is too long")

    async for session in get_db():
        stmt = (
            select(Question)
            .where(Question.name == question_name)
            .where(Question.scope.has(name=scope))
        )
        question = (await session.execute(stmt)).scalars().first()
        if not question:
            raise ValueError("Question not found")

        # TODO: Handle multiple input and output
        input_and_output: InputAndOutput = question.input_and_outputs[0]

    with httpx.Client(base_url=SANDBOX_URL) as client:
        try:
            r = client.post(
                "/",
                json={
                    "code": code,
                    "input": input_and_output.input,
                },
                timeout=TIMEOUT,
            )
        except httpx.TimeoutException:
            return "### Backend timeout", "error"
        if r.status_code != 200:
            return "### Unknown error", "error"
        result = r.json()
        status = Result(result["status"])
        msg = result["msg"]
        print(f"{code}\n{result['status']}\n{msg}")
        if status == Result.SUCCESS:
            # TODO: Handle the message
            msg = bytes.fromhex(msg)
            if msg.strip() == input_and_output.output.strip().encode():
                return "### Your code results: AC", "AC"
            return "### Your code results: WA", "WA"
        elif status == Result.RUNTIME_ERROR:
            # TODO: Maybe need to escape the message before rendering
            return f"### Your code results: {result['status']}\n{bytes.fromhex(msg)}", "RE"

        text = await code_advice(f"{code}\n{result['status']}\n{msg}")
        return f"### Your code results: {result['status']}\n{msg}", text

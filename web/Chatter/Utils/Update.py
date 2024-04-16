# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""

import gradio as gr
from sqlalchemy import select

from Chatter.Database.connection import get_db
from Chatter.Database.models import Question

async def get_question_description(scope_name: str, question_name: str) -> gr.Markdown:
    description = None

    async for session in get_db():
        # select where question have same name and scope name
        stmt = (
            select(Question)
            .where(Question.name == question_name)
            .where(Question.scope.has(name=scope_name))
        )
        question: Question | None = (await session.execute(stmt)).scalars().first()
        if question:
            description = question.description
            if description:
                return gr.Markdown(description)

    return gr.Markdown("No description found for this question.")

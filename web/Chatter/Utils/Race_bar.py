
from Chatter.Database.connection import get_db
from Chatter.Database.models import Question, Scope, Submission
import asyncio
import gradio as gr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Chatter.Utils.Update import get_submissions
import pandas as pd
# 假设你已经定义了Submission模型和get_db函数

async def print_submissions():
    # 异步函数需要在事件循环中运行
    submissions = await get_submissions(30, 0)  # 示例：获取第1页，每页10条
    df = pd.DataFrame(
        [
            [submission.id,  submission.user.username,submission.question.scope.name , submission.question.scope_id, submission.status, submission.created_at] 
            for submission in submissions
        ], 
        columns=["ID", "Name", "Scope", "Question", "Status", "Time"]
    )
    return df

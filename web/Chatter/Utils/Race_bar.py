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
    # 转换日期时间格式
    df["Time"] = pd.to_datetime(df["Time"])

    # 去除毫秒部分，只保留整数秒
    df["Time"] = df["Time"].dt.floor('s')

    # 转换为 UTC+8
    df["Time"] = df["Time"].dt.tz_convert('Asia/Shanghai')
    return df

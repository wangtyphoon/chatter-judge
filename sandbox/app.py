import os
import subprocess
import tempfile
from enum import Enum

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel


class RunCode(BaseModel):
    code: str
    input: str


class Result(str, Enum):
    SUCCESS = "success"
    COMPILE_TIME_ERROR = "compile_time_error"
    RUNTIME_ERROR = "runtime_error"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"


TIMEOUT = 8

app = FastAPI()


@app.post("/")
def run(run_code: RunCode, background_tasks: BackgroundTasks):
    try:
        compile(run_code.code, "string", "exec")
    except Exception as e:
        return Result.COMPILE_TIME_ERROR, str(e)

    temp_file = tempfile.mktemp()

    with open(temp_file, "w") as f:
        f.write(run_code.code)

    try:
        p = subprocess.run(
            [
                "nsjail",
                "-Q",
                "--config",
                "/home/user/nsjail.cfg",
                "-R",
                f"{temp_file}:/home/user/run.py",
                "--",
                "/usr/bin/python3",
                "/home/user/run.py",
            ],
            input=run_code.input.encode(),
            capture_output=True,
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        os.remove(temp_file)
        return Result.TIME_LIMIT_EXCEEDED, ""

    background_tasks.add_task(os.remove, temp_file)

    if p.returncode == 0:
        return {"status": Result.SUCCESS, "msg": p.stdout.hex()}
    return {"status": Result.RUNTIME_ERROR, "msg": p.stderr.hex()}

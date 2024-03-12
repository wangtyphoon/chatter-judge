# -*- coding: utf-8 -*-
"""
Create Date: 2023/10/18
Author: @1chooo (Hugo ChunHo Lin)
Version: v0.0.1
"""
import json
import os

import requests

API_KEY = os.environ.get("GEMINI_API_KEY")


async def respond(
    message,
    chat_history,
    *args,
    **kwargs,
):
    # 定義對話狀態 (conversation_state)
    conversation_state = {
        "contents": [],
        "safety_settings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ],
    }

    # 生成回應函式 (generate_response)
    def generate_response(data):
        # 建構 API 請求 URL
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

        # 設定 JSON 內容的標頭 (headers)
        headers = {"Content-Type": "application/json"}

        # 使用 requests 函式送出 POST 請求至 API
        response = requests.post(url, headers=headers, json=data)

        # 解析來自 API 的 JSON 回應，並格式化以方便閱讀
        json_response = json.dumps(response.json(), indent=4, ensure_ascii=False)

        return json_response

    # 模型回應函式 (model_response)
    def model_response(text):
        data = {
            "role": "model",  # 指定角色為模型 (model)
            "parts": [{"text": f"{text}"}],  # 文字內容包含在 "text" 欄位
        }
        return data

    # 使用者輸入函式 (user_word)
    def user_word(text):
        data = {
            "role": "user",  # 指定角色為使用者 (user)
            "parts": [{"text": f"{text}"}],  # 文字內容包含在 "text" 欄位
        }
        return data

    # 對話歷史初始化
    def init_dialog(sentence):
        for i in sentence:
            user_input = user_word(i[0])
            model_output = model_response(i[1])
            conversation_state["contents"].append(user_input)
            conversation_state["contents"].append(model_output)

    init_dialog(chat_history)

    # 將使用者輸入轉換成符合格式的資料 (user_word)
    user_input = user_word(message)

    # 更新對話狀態 (conversation_state)
    conversation_state["contents"].append(user_input)

    # 生成對使用者輸入的回應 (generate_response)
    response = generate_response(conversation_state)

    # 解析來自 API 的 JSON 回應 (response_data)
    response_data = json.loads(response)

    # 解析來自 API 的 JSON 回應 (response_data)
    try:
        generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        raise ValueError(f"API response error: {response_data}")
    print(f"Gemini：{generated_text}")
    print(f"chat_history: {chat_history}")

    return generated_text

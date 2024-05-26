import google.generativeai as genai
import os
# 從環境變數讀取 API 金鑰
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY 環境變數未設置")

async def schdule(
    message,
    *args,
    **kwargs,
    ):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    }


    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    prompt_parts = [ "請根據使用者的訊息，將問題的難度分為簡單與困難兩類，困難的問題是負責解決高邏輯思考或是沒有標準答案的問題",     
                    "input: " + message,
                    "output: ",]
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
    
    response = model.generate_content(prompt_parts)
    print(response.text)
    return response.text
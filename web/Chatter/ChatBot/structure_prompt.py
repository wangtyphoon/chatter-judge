"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import os

import google.generativeai as genai


async def structured_prompt(message):
    # 從環境變數讀取 API 金鑰
    API_KEY = os.environ.get("GEMINI_API_KEY")

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY 環境變數未設置")

    genai.configure(api_key=API_KEY)
    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    prompt_parts = [
        "請根據給予的程式碼，程式碼的運行狀態與訊息，請簡潔的給予問題分析與簡潔的程式碼改進建議(繁體中文)，不需要展示程式碼",
        "input: year = float(input('请输入年份: '))\nis_leap == year % 4 == 0 and year % 100 != 0 or year % 400 == 0\nprint(is_leap)\nruntime_error\nNameError: name 'is_leap' is not defined",
        "output: ## 問題分析：\n\n程式碼出現 `NameError`，原因是使用了未定義的變數 `is_leap`。應是 `==` 符號誤用，導致變數賦值操作 (`=`) 沒有執行。\n\n\n## 改進建議：\n\n將 `is_leap ==` 修改為 `is_leap =` 即可。",
        'input: import math\n\ndef calculate_triangle_properties(a, b, c):\n    """\n    計算三角形的周長和面積\n\n    參數:\n    a (float): 第一條邊長\n    b (float): 第二條邊長\n    c (float): 第三條邊長\n\n    返回:\n    tuple: 包含周長和面積的元組 (perimeter, area)，如果無法構成三角形，則返回 None\n    """\n    perimeter = a + b + c\n    s = perimeter / 2\n    area = math.sqrt(s * (s - a) * (s - b) * (s - c))\n    return perimeter, area\n\n# 輸入三條邊長\na = float(input("請輸入第一條邊長: "))\nb = float(input("請輸入第二條邊長: "))\nc = float(input("請輸入第三條邊長: "))\n\n# 計算三角形的周長和面積\nperimeter, area = calculate_triangle_properties(a, b, c)\nprint("三角形的周長為:", perimeter)\nprint("三角形的面積為:", area)\nsuccess\nWA',
        "output: ## 問題分析：\n\n程式碼缺少判斷輸入的三邊長是否能構成三角形的邏輯。\n\n## 改進建議：\n\n1. **加入三角形判斷**: 在計算周長和面積之前，加入判斷式，檢查三邊長是否滿足三角形法則 (任意兩邊之和大於第三邊)。\n2. **處理非法輸入**: 如果輸入無法構成三角形，則返回 `None` 或輸出錯誤訊息。",
        'input: def print_triangle(height):\n    if height == 0:\n        return\n    print_triangle(height - 1)\n    print("*" * height)\n\n# 輸出一個高度為 10000 的三角形金字塔\nprint_triangle(10000)\ntime_limit_exceed',
        "output: ## 問題分析\n\n程式碼使用遞迴方式印出三角形，但當高度過大 (例如 10000) 時，會超出系統堆疊限制，導致執行時間過長或崩潰。\n\n## 改進建議\n\n1. **使用迴圈**: 將遞迴改寫為迴圈，避免堆疊溢位問題。\n2. **優化輸出**: 可考慮使用字串拼接，一次性輸出，減少輸出次數，提高效率。",
        "input: import math\n\nfor num in range(2, 100):\n    is_prime = True\n    for factor in range(2, int(math.sqrt(num)) + 1):\n        if num % factor == 0:\n            is_prime = False\n            break\n    if is_prime:\n        print(num, end=' ')\ncompile_error\nModuleNotFoundError: No module named 'math'",
        "output: ## 問題分析\n\n程式碼出現 `ModuleNotFoundError`，表明 Python 找不到名為 `math` 的模組。\n\n## 改進建議\n\n1. **確認安裝**: 檢查是否已安裝 `math` 模組。可以使用 `pip list` 命令查看已安裝的模組列表。\n2. **安裝模組**: 若未安裝，使用 `pip install math` 命令安裝 `math` 模組。\n3. **檢查環境**: 若在虛擬環境中，確保在正確的環境中安裝和運行程式碼。",
        "input: primes = []\nfor num in range(2, 100):\n  is_prime = True\n  for factor in range(2, num):\n    if num % factor == 0:\n      is_prime = False\n      break\n  if is_prime:\n    primes.append(num)\nprint(primes)\nsuccess\nWA",
        "output: ## 問題分析：\n\n程式碼的目標是找出 2 到 100 之間的質數，但判斷質數的邏輯存在錯誤。目前的程式碼會將所有數字都判斷為質數，因為 `factor` 的範圍是從 1 到 `num-1`，而任何數字都能被 1 整除。\n\n## 改進建議：\n\n1. **修改 `factor` 的範圍**: 將 `factor` 的範圍修改為從 2 到 `num` 的平方根，因為一個數如果不能被 2 到其平方根之間的任何整數整除，那它就是質數。\n2. **優化判斷條件**: 可以優化判斷條件，當找到一個能整除的 `factor` 時，直接跳出迴圈，避免不必要的計算。",
        "input: def is_palindrome(num):\n    num_str = str(num)\n    reversed_num_str = num_str[::-1]\n    return num_str == reversed_num_str\nsuccess\nWA",
        "output: ## 問題分析與改進建議\n\n**問題:** 程式碼邏輯正確，但可能未通過所有測試案例，導致 WA (Wrong Answer) 結果。\n\n**可能原因:**\n\n* **未考慮負數：** 負數的反轉與正數不同，例如 `-121` 的反轉應為 `-121` 而不是 `121-`。\n* **未考慮前導零：** 數字 `012` 應視為 `12`，但程式碼可能將其視為不同的數字。\n\n**改進建議:**\n\n1. **處理負數：** 在轉換為字串前，先取絕對值 `abs(num)`，確保處理的是正數。\n2. **處理前導零：** 使用 `int(num_str)` 將字串轉回數字，去除前導零。",
        'input: def is_palindrome(num):\n    """判斷一個數是否是回文數"""\n    temp = num\n    total = 0\n    while temp > 0:\n        total = total * 10 + temp % 10\n        temp //= 10\n    return total == num\nsuccess\nAC',
        "output: ## 程式碼分析與改進建議\n\n**分析：** 程式碼的功能是判斷一個數是否為回文數，實現方法是將數字反轉後與原數字比較。\n\n**改進建議：**\n\n* **字串操作：** 可以考慮將數字轉換為字串，利用字串切片功能反轉字串，再與原字串比較，這樣可以簡化程式碼。\n* **遞迴函數：** 可以使用遞迴函數來實現數字反轉，這樣可以使程式碼更加簡潔優雅。\n* **效能：** 如果需要處理大量數字或大型數字，可以考慮使用更高效的演算法，例如利用數學特性來判斷回文數。",
        'input: def get_file_extension(file_name):\n """\n 取得檔案的副檔名\n\n Args:\n  file_name: 檔案名稱，包含副檔名\n\n Returns:\n  副檔名，若無副檔名則回傳空字串\n """\n # 使用 rsplit() 從右側分割檔名，最多分割一次\n # 取得副檔名\n file_extension = file_name.split(\'.\', 1)[-1]\n return file_extension\nsuccess \nWA',
        "output: ## 問題分析：\n\n程式碼邏輯看似正確，但 `WA` 提示可能代表在某些邊界情況下出錯。\n\n## 改進建議：\n\n1. **檢查空檔名情況**: 若 `file_name` 為空字串，`rsplit` 會返回 `['']`，導致 `[-1]` 取值錯誤。應在分割前檢查 `file_name` 是否為空。\n2. **考慮無副檔名情況**: 若檔名無 `.`，`rsplit` 會返回原字串，導致錯誤的副檔名。應檢查分割後的列表長度，若為 1 則代表無副檔名，應返回空字串。",
        "input: persons = [True] * 30\ncounter, index, number = 0, 0, 0\nwhile counter < 15:\n  if persons[index]:\n    number += 1\n    if number == 9:\n      persons[index] = False\n      counter += 1\n      number = 0\n  index += 1\n  print(persons)\nfor person in persons:\n  print('基' if person else '非', end='')\nruntime_error",
        'output: ## 問題分析：\n\n程式碼的目的是從 30 個人中挑選 15 個人，每隔 8 個人淘汰第 9 個人。 錯誤訊息 "runtime_error" 顯示程式運行時出現問題。\n\n主要問題在於 `index` 變數可能超出 `persons` 列表的索引範圍 (30)，導致錯誤。\n\n## 改進建議：\n\n1. **限制 `index` 範圍**: 在每次 `index += 1` 後，檢查 `index` 是否達到 30。如果達到，將 `index` 重置為 0，使其回到列表開頭。\n2. **結束條件**: 目前的結束條件是 `counter < 15`，但有可能在淘汰 15 人之前，`index` 就已經循環完整個列表。建議增加一個條件，例如設定一個最大循環次數，避免無限循環。',
        'input: import math\nclass Point:\n  """\n  描述平面上的点的类\n  """\n  def __init__(self, x=0, y=0):\n    """\n    初始化点的坐标\n\n    Args:\n      x: 横坐标\n      y: 纵坐标\n    """\n    self.x = x\n    self.y = y\n\n  def move(self, dx, dy):\n    """\n    移动点的位置\n\n    Args:\n      dx: 横向移动距离\n      dy: 纵向移动距离\n    """\n    self.x += dx\n    self.y += dy\n\n  def __distance_to(self, other_point):\n    """\n    计算到另一个点的距离\n\n    Args:\n      other_point: 另一个 Point 对象\n\n    Returns:\n      到另一个点的距离\n    """\n    dx = self.x - other_point.x\n    dy = self.y - other_point.y\n    return math.sqrt(dx**2 + dy**2)\np1 = Point(3,4)\nP2 = Point()\np1.distance_to(P2)\ncompile_error\nAttributeError: \'Point\' object has no attribute \'distance_to\'',
        "output: 問題分析：\n程式碼出現 AttributeError，顯示 Point 物件沒有 distance_to 屬性。這是因為 __distance_to 方法使用了兩個底線開頭的命名方式，這在 Python 中代表私有方法。私有方法無法直接從物件外部調用。\n\n改進建議：\n移除 __distance_to 方法名稱中的雙底線： 將方法名稱改為 distance_to，使其成為公開方法，即可從外部調用。\n(可選) 使用 @property 裝飾器： 若希望像訪問屬性一樣調用 distance_to 方法，可以使用 @property 裝飾器將其轉換為屬性。",
        "input: " + message,
        "output: ",
    ]

    response = model.generate_content(prompt_parts)
    print(response.text)
    return response.text

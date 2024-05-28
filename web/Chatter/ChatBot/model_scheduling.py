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
                    "input: 哈囉",
                    "output: 簡單",
                    "input: 你好",
                    "output: 簡單",
                    "input: Hi",
                    "output: 簡單",
                    "input: 是否能幫忙翻譯以下文字：While physically accumulations (from event onset to termination) provide a more fundamental connection between the moisture budget and precipitation pdfs, in practice precipitation aggregated over fixed time intervals (e.g., daily precipitation) is the main object of the research community interest. An important distinction between event accumulation and daily precipitation is that the accumulation only depends on dynamics occurring while precipitating whereas daily precipitation mixes dynamics occurring at wet and dry times. This distinction has an important imprint in the resulting accumulation and daily precipitation pdfs. Figure 4 shows the typical shape of these pdfs for one location in the tropics (Fig. 4a) and one location in midlatitudes (Fig. 4b). In both cases pdfs display a power law range for low and moderate values and a cutoff scale where the probability drops much faster, in agreement with the stochastic prototype for accumulations. The main difference is the gentler power law exponent τP for daily precipitation (τP < τ), which can be explained using the stochastic prototype for accumulations as a starting point. Under suitable conditions for the length of accumulation events with respect to the averaging interval (e.g., 1 day for daily precipitation), daily precipitation is approximately the summation of individual accumulation events within a day. This reduces daily precipitation power law exponent because days with multiple accumulation events contribute to a larger probability of higher daily precipitation amounts at the expense of low and moderate amounts, flattening the power law range (Martinez-Villalobos and Neelin 2019).",
                    "output: 簡單",
                    "input: 是否能幫忙翻譯並解出以下題目?Prove that the fractional knapsack problem has the greedy-choice property.",
                    "output: 困難",
                    "input: 是否能幫忙翻譯以下題目?Prove that the fractional knapsack problem has the greedy-choice property.",
                    "output: 簡單",
                    "input: 是否能幫忙解以下題目?Give a dynamic-programming solution to the 0-1 knapsack problem that runs in \nO(nW)time, where n is the number of items and W is the maximum weight of \nitems that the thief can put in the knapsack.",
                    "output: 困難",
                    "input: 如果我想用python做貪吃蛇小遊戲，我應該怎麼寫程式碼?",
                    "output: 困難",
                    "input: 以下是我的程式碼：\ndef merge(A, p, q, r):\n    #定義subarray的邊界與建立subarray(divide)。此為python程式碼，A為list型態\n    n_L = q - p + 1\n    n_R = r - q\n    L = []\n    R = []\n    for i in range(n_L):\n        L[i] = A[p+i]\n    for j in range(n_R):\n        R[j] = A[q+j+1] \n    \n    i = 0\n    j = 0\n    k = p\n    #比大小~小的先排\n    while i < n_L and j < n_R:\n        if L[i] <= R[j]:\n            A[k] = L[i]\n            i += 1\n        else:\n            A[k] = R[j]\n            j += 1\n        k += 1\n\n    \n    #剩餘元素處理\n    while i < n_L:\n        A[k] = L[i]\n        i += 1\n        k += 1\n\n    while j < n_R:\n        A[k] = R[j]\n        j += 1\n        k += 1\n最後此程式碼會有out of index的問題。想請問該如何解?",
                    "output: 簡單",
                    "input: 我可以如何寫一個python code，讓他能從1印到100?",
                    "output: 簡單",
                    "input: 我可以如何用python爬以下檔案?\nhttps://www.cwa.gov.tw/Data/radar/CV1_3600_202405141950.png",
                    "output: 困難",
                    "input: 中壢有什麼好吃的嗎?",
                    "output: 簡單",
                    "input: 是否能幫我把以下心得拉長到5000字?\n\n\n天氣，一直不斷地在我們身邊發生，在我們的生活上，扮演著不可或缺的角色，從每天的穿搭，到對於劇烈天氣的防範，甚至於我們的生命，都與天氣脫離不了干係。然而，儘管進了大氣系，對於許多許多與天氣相關的事務，我幾乎都還不了解，而天氣學的秘密(一)、(二)，則帶給了我新穎、更多的知識了解大氣。\n\n    影片大概是講述一群對天氣熱愛的人從美國東岸飛到美國西岸間的故事。數個科學家從美國佛羅里達州出發，並在海上測量了一朵雲的體積、重量(同時，又有兩位勇者從高空跳傘，並體驗、尋找出了把水氣上推的力)，然後，又猜想了下雨的機制-是否含有生命體的水更容易結冰(而在地上的科學家也拿了三組水-純水、含礦物質的水與含生命體的水，將其至於0度以下之環境中，看誰先結冰，中為含生命體的水先結冰)；接著，在墨西哥灣沿岸，科學家們又探討了候鳥南渡墨西哥灣的機制(候鳥常在鋒面過後順著風前往中南美洲過冬)。之後，一行人來到德克薩斯州的工業大鎮-休士頓的上空，探討了空氣汙染對於海溫、凝結核等影響，以探討近年颶風強度、數量上升的原因。接著進入下集，開頭先是研究在極高空中是否有生命(同時又有勇者跳傘，收集高空中的生命體)，之後大致介紹了一下沙漠大氣的運動後，便來到的\n亞利桑納州的首府-鳳凰城，了解一個城市如何創造自己的氣候。最後，一行人穿越了洛磯山脈，來到了加州沿岸，並在探索完當地海洋物產豐饒的原因後，結束了行程。\n\n    看完了這兩部影片，我發現，原來天氣對我們及各種生物的影響，遠遠超乎我的想像。從高空中的生命，到候鳥的遷徙，都逃不出天氣的掌控，只要天氣(或大氣)條件出了什麼狀況，都會對生物造成極為嚴重的影響，例如:如果候鳥南遷時間錯誤，那麼逆風有可能使牠在抵達陸地前便筋疲力竭，以至於其死於遷徙的路途上。再如，美西海岸(東北太平洋一帶)中，海底世界多采多姿的的生命亦歸功於大氣(以及海洋)的影響，若不是它們，美西濱海還不一定有如此豐沛的生物資源呢!\n\n    另外，在這兩部影片中，我也發現了有趣卻又可能真實的科普小知識(或推測)，如:如何測一朵雲的重量、一朵雲多重，並從而推出地球上有許多水資源是儲藏在大氣中的，又或是廢氣的排放有可能抑制熱帶風暴的生成，改善廢氣排放反而可能使熱帶報的數量增加(實為恢復常態);另外，在這部影片中，我也了解到了要收集某些資料並不是那麼的輕鬆，例如在影片中，為了收集某些在高空中的樣本，收集者必須從數公里高的高空中跳下來，而且只要出一點差錯，不僅可能收不了預期要收的資料，甚至有可能危害到自己的性命，因此我也佩服他們(資料收集者)的精神。\n\n    雖然之前在地球科學系統概論時，已經有看過天氣學的秘密(一)了，但這一次再看，不僅對過去的內容有了更深的印象，同時又看了天氣學的秘密(二)，使影片更具有連貫性，也更看得懂這部紀錄片的意義。感謝老師放的這部影片，使我對大氣有更多的理解。",
                    "output: 簡單",
                    "input: 是否能幫忙整理以下文章並抓出重點?\n不得檢出值不是零 \n三聚氰胺及萊克多巴胺之標準為不得檢出（Non-Detected），但不\n得檢出值分別為 2.5 ppm（食品）及 1 ppb（動物用藥殘留標準）以下，\n竟然不是 0，您沒看（聽）錯，確實不是 0。仔細探究，其中竟有耐\n人尋味之處，就像松露巧克力不含松露，阿拉伯數字不是阿拉伯人發\n明的一樣，人們常直觀的望文生義，以為零檢出（zero tolerance）、不\n得檢出之檢測值應該是 0。非也，因必須應用儀器及檢測方法來檢測\n污染物，即使是不含污染物的試劑水，檢測實務上儀器必定會產生訊\n號，有訊號必定會轉換成檢測值，故不得檢出值不會是零。",
                    "output: 簡單",
                    "input: 如果我今天有100元，每多一天會增加10倍，請問一個月後我有多少錢?我可以如何用程式表達?",
                    "output: 簡單",
                    "input: 台北有什麼美食",
                    "output: 簡單",
                    "input: 如何實作一個binary search tree?",
                    "output: 困難",
                    "input: 如何用python實作Dijkstra algorithm?",
                    "output: 困難",
                    "input: 如何以python實作一個stack?",
                    "output: 簡單",
                    "input: 如何以python判斷質數合數?",
                    "output: 簡單",
                    "input: 想請問網路分為哪幾層?",
                    "output: 簡單",
                    "input: 想請問如何使用python算直角三角形邊長?",
                    "output: 簡單",
                    "input: 想請問如何使用html、javascript、資料庫等架設登入系統",
                    "output: 困難",
                    "input: 想請問何謂物件導向?如何以python實作之?",
                    "output: 簡單",
                    "input: 想請問如何以程式語言實作queue?",
                    "output: 簡單",
                    "input: 是否能說明如何使用for迴圈?",
                    "output: 簡單",
                    "input: 是否能說明如何使用if、else判斷式?",
                    "output: 簡單",
                    "input: 如何使用matplotlib.pyplot繪製圖片?每行的程式又代表什麼意義?",
                    "output: 簡單",
                    "input: 如何使用pygame實作背景音樂?",
                    "output: 簡單",
                    "input: 如何利用html、javascript做出跑馬燈效果?",
                    "output: 簡單",
                    "input: 如何利用python進行微分運算?",
                    "output: 簡單",
                    "input: 如何用python做出單位矩陣?",
                    "output: 簡單",
                    "input: 如何利用python進行cifar10進實作模型訓練與圖片分類",
                    "output: 困難",
                    "input: 在python中如何尋找list中元素的最大值?",
                    "output: 簡單",
                    "input: 如何利用python進行積分運算?",
                    "output: 簡單",
                    "input: 如何使用python讀取資料?",
                    "output: 簡單",
                    "input: 如何使用python中的pandas套件去讀取資料?",
                    "output: 簡單",
                    "input: 如何取出pandas讀取檔案中的特定資料?",
                    "output: 簡單",
                    "input: 現在手上有一份資料，如何利用python寫進檔案?",
                    "output: 簡單",
                    "input: 如何使用python做傅立葉分析?",
                    "output: 簡單",
                    "input: 如何使用python實作機器學習-房價預測",
                    "output: 困難",
                    "input: 如何實作quick sort?",
                    "output: 簡單",
                    "input: 我想要將以下資料依照數字大小或字元ASCII碼大小去排序，我可以怎麼寫程式?",
                    "output: 簡單",
                    "input: 請問何謂指標?如何實作?",
                    "output: 簡單",
                    "input: 明天會不會下雨?",
                    "output: 簡單",
                    "input: 在C語言中，如果我想在function中傳入陣列，我可以如何去實作?",
                    "output: 簡單",    
                    "input: " + message,
                    "output: ",]
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
    
    response = model.generate_content(prompt_parts)
    print(response.text)
    return response.text
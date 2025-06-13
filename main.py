from typing import Optional

from fastapi import FastAPI

from fastapi.responses import HTMLResponse

import random

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/omikuji")
def omikuji():
    omikuji_list = [
        "大吉",
        "中吉",
        "小吉",
        "吉",
        "半吉",
        "末吉",
        "末小吉",
        "凶",
        "小凶",
        "大凶"
    ]
    
    return {"result" : omikuji_list[random.randrange(10)]}

@app.get("/index")
def index():
    html_content = """
    <!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>適当ランダムページ</title>
  <style>
    /* 全体のフォントとレイアウト */
    body {
      margin: 0;
      padding: 0;
      font-family: "Segoe UI", sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      transition: background-color 0.5s ease;
    }
    h1 {
      font-size: 3rem;
      margin-bottom: 0.5rem;
    }
    p.quote {
      font-size: 1.5rem;
      font-style: italic;
      text-align: center;
      max-width: 80%;
    }
    button {
      padding: 0.5rem 1rem;
      font-size: 1rem;
      cursor: pointer;
      border: none;
      border-radius: 0.25rem;
      background-color: rgba(255,255,255,0.8);
      transition: background-color 0.3s;
    }
    button:hover {
      background-color: rgba(255,255,255,1);
    }
  </style>
</head>
<body>
  <h1 id="title">適当な見出し</h1>
  <p class="quote" id="quote">“何かしら適当に…”</p>
  <button id="shuffle">もう一度ランダム</button>

  <script>
    // ランダムに選ぶ背景色の候補
    const colors = [
      "#FFB3BA","#FFDFBA","#FFFFBA","#BAFFC9","#BAE1FF",
      "#C8A2C8","#F4C2C2","#E0FFFF","#FFE4E1","#FFFACD"
    ];

    // ランダムに選ぶタイトルの候補
    const titles = [
      "今日はなんとなく…",
      "適当万歳！",
      "気まぐれページ",
      "ランダム万歳",
      "行き当たりばったり"
    ];

    // ランダムに選ぶ名言（正式出典ではありません、適当に）
    const quotes = [
      "“人生は適当に歩けばいい。”",
      "“偶然こそ人生の醍醐味。”",
      "“完璧なんて求めない。”",
      "“適当にやれば楽になる。”",
      "“ミスこそ次へのステップ。”"
    ];

    // 要素取得
    const body    = document.body;
    const titleEl = document.getElementById("title");
    const quoteEl = document.getElementById("quote");
    const btn     = document.getElementById("shuffle");

    // ランダム更新関数
    function shuffleAll() {
      // 背景色ランダム設定
      const color = colors[Math.floor(Math.random() * colors.length)];
      body.style.backgroundColor = color;

      // タイトルランダム設定
      titleEl.textContent = titles[Math.floor(Math.random() * titles.length)];

      // 名言ランダム設定
      quoteEl.textContent = quotes[Math.floor(Math.random() * quotes.length)];
    }

    // 初回実行
    shuffleAll();

    // ボタン押下で再ランダム
    btn.addEventListener("click", shuffleAll);
  </script>
</body>
</html>

    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/present")
async def give_present(present):
    return {"response": f"サーバです。メリークリスマス！ {present}ありがとう。お返しはキャンディーです。"}  # f文字列というPythonの機能を使っている

from typing import Optional

from fastapi import FastAPI

from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


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
  <title>時間で変化するアート</title>
  <style>
    body, html {
      margin: 0; padding: 0;
      width: 100%; height: 100%;
      overflow: hidden;
      background-color: #000;
    }
    canvas {
      display: block;
    }
  </style>
</head>
<body>
  <canvas id="art"></canvas>
  <script>
    // ────────── 初期設定 ──────────
    const canvas = document.getElementById('art');
    const ctx = canvas.getContext('2d');
    // 解像度調整（devicePixelRatioで高DPI対応）
    function resize() {
      const dpr = window.devicePixelRatio || 1;
      canvas.width  = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.scale(dpr, dpr);
    }
    window.addEventListener('resize', resize);
    resize();

    // ────────── ユーティリティ関数 ──────────
    /** 0〜1 の値を受け取って、指定範囲の線形補間を返す。\
     *  Tip: 線形補間（lerp）は、二点間を t (0–1) で補間する手法。 */
    function lerp(a, b, t) {
      return a + (b - a) * t;
    }

    /** HSV→RGB 変換。\
     *  Tip: HSV (色相・彩度・明度) 表色系は、色相(hue)を角度で管理。 */
    function hsvToRgb(h, s, v) {
      let c = v * s;
      let x = c * (1 - Math.abs((h / 60) % 2 - 1));
      let m = v - c;
      let rgb;
      if (h < 60)      rgb = [c, x, 0];
      else if (h < 120) rgb = [x, c, 0];
      else if (h < 180) rgb = [0, c, x];
      else if (h < 240) rgb = [0, x, c];
      else if (h < 300) rgb = [x, 0, c];
      else              rgb = [c, 0, x];
      return rgb.map(v => Math.round((v + m) * 255));
    }

    // ────────── アニメーション変数 ──────────
    let startTime = null;

    // ────────── 描画ループ ──────────
    function draw(now) {
      if (!startTime) startTime = now;
      const t = (now - startTime) / 1000; // 経過秒数

      const W = window.innerWidth;
      const H = window.innerHeight;
      const cell = 50;         // 一つの四角形のサイズ
      const cols = Math.ceil(W / cell);
      const rows = Math.ceil(H / cell);

      // 背景クリア
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, W, H);

      // グリッド描画
      for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
          const x = i * cell;
          const y = j * cell;
          // 各セルごとに位相をずらす
          const phase = Math.sin((i + j) * 0.5 + t * 1.2);
          // 色相を時間で変化させる
          const hue = (t * 30 + phase * 60 + i * 5) % 360;
          const sat = lerp(0.4, 1.0, (phase + 1) / 2);
          const val = lerp(0.3, 1.0, (Math.cos(phase + t) + 1) / 2);
          const [r, g, b] = hsvToRgb(hue, sat, val);
          ctx.fillStyle = `rgb(${r},${g},${b})`;

          // 円の大きさも時間で変化
          const radius = cell * 0.4 * ((phase + 1) / 2);
          ctx.beginPath();
          ctx.arc(x + cell/2, y + cell/2, radius, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // 次フレーム
      requestAnimationFrame(draw);
    }

    requestAnimationFrame(draw);
  </script>
</body>
</html>

    """
    return HTMLResponse(content=html_content, status_code=200)

class PresentRequest(BaseModel):
    name: str = Field(..., description="贈り物をくれた人の名前")
    gift: str = Field(..., description="贈り物の名前")
    meta: Dict[str, Any] = Field(default_factory=dict, description="追加情報")

# 簡易キャッシュ（メモリ上）
request_history = []

# バックグラウンドタスク：履歴を追加
def log_request(data: dict):
    # 最大履歴数を100件に制限
    if len(request_history) >= 100:
        request_history.pop(0)
    request_history.append({**data, "logged_at": datetime.utcnow().isoformat()})

@app.post("/present")
async def give_present(
    request: PresentRequest,
    background_tasks: BackgroundTasks
):
    # リクエスト内容を辞書化
    req_data = request.dict()
    # バックグラウンドで履歴に保存
    background_tasks.add_task(log_request, req_data)
    # タイムスタンプ付きレスポンス生成
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # お返しメッセージをランダム化
    candy = ["チョコレート","キャンディー","クッキー"]
    reply = f"メリークリスマス！ {request.name}さん、{request.gift}ありがとう。お返しは{candy[hash(request.name) % len(candy)]}です。 ({timestamp})"
    return {"response": reply, "history_count": len(request_history)}

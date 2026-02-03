import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

CATEGORY_LABELS = {
    "prompt": "AIプロンプト集",
    "notion": "Notionテンプレート",
    "canva": "Canvaテンプレート",
    "ebook": "電子書籍",
    "excel": "Excelテンプレート",
    "spreadsheet": "スプレッドシート",
    "powerpoint": "PowerPointテンプレート",
    "figma": "Figmaテンプレート",
    "checklist": "チェックリスト/ワークシート",
    "linestamp": "LINEスタンプ",
    "icon": "アイコンセット",
    "course": "オンラインコース",
}

PRICE_RANGES = {
    "prompt": (980, 2980),
    "notion": (500, 1500),
    "canva": (800, 2000),
    "ebook": (500, 1980),
    "excel": (500, 1500),
    "spreadsheet": (500, 1500),
    "powerpoint": (800, 2000),
    "figma": (1500, 5000),
    "checklist": (300, 980),
    "linestamp": (120, 480),
    "icon": (500, 2000),
    "course": (3000, 30000),
}


def generate_with_gemini(category: str, target: str, additional_notes: str = ""):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return generate_mock(category, target)

    category_label = CATEGORY_LABELS.get(category, "デジタル商品")
    price_min, price_max = PRICE_RANGES.get(category, (980, 1980))

    prompt = f"""あなたはGumroadで月100万円以上稼ぐトップセラーのデジタル商品クリエイターです。
売れる商品を提案してください。

【商品カテゴリ】{category_label}
【ターゲット】{target}
{f"【追加要望】{additional_notes}" if additional_notes else ""}

以下のJSON形式のみで出力してください（日本語で、説明文なし）:
{{
  "productNames": ["魅力的な商品名1", "魅力的な商品名2", "魅力的な商品名3"],
  "description": "購買意欲を刺激する200-300文字の商品説明文。ベネフィットを明確に。",
  "suggestedPrice": {price_min}から{price_max}の間の最適価格（整数のみ）,
  "tags": ["検索されやすいタグ1", "タグ2", "タグ3", "タグ4", "タグ5"]
}}

【重要ルール】
- 商品名は具体的な数字や成果を含める（例：「30日で〇〇」「〇〇が10倍になる」）
- 説明文は「あなた」に語りかける形式で、悩みと解決策を明示
- タグはGumroad検索で上位表示されやすいキーワードを選定
- JSONのみを出力"""

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 1024},
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            response_text = result["candidates"][0]["content"]["parts"][0]["text"]

            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            json_str = response_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        print(f"Gemini API error: {e}")
        return generate_mock(category, target)


def generate_mock(category: str, target: str):
    category_label = CATEGORY_LABELS.get(category, "デジタル商品")
    price_min, price_max = PRICE_RANGES.get(category, (980, 1980))
    avg_price = (price_min + price_max) // 2

    return {
        "productNames": [
            f"【保存版】{target}のための{category_label}",
            f"{target}必見！即実践{category_label}",
            f"初心者OK！{target}向け{category_label}完全ガイド",
        ],
        "description": f"「{target}」の方に向けた{category_label}です。\n\n"
        f"このテンプレートを使えば、面倒な作業を大幅に短縮できます。\n"
        f"初心者でもすぐに使い始められるよう、わかりやすい説明付き。\n\n"
        f"【含まれる内容】\n"
        f"・すぐに使えるテンプレート一式\n"
        f"・カスタマイズガイド\n"
        f"・活用事例集",
        "suggestedPrice": avg_price,
        "tags": [target, category_label, "テンプレート", "時短", "初心者向け"],
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "healthy"}).encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            category = data.get("category", "prompt")
            target = data.get("target", "")
            additional_notes = data.get("additionalNotes", "")

            result = generate_with_gemini(category, target, additional_notes)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

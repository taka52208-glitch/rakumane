import json
import os
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


def generate_product(category: str, target: str, additional_notes: str = None):
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

            result = generate_product(category, target, additional_notes)

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

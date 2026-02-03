import json
import os
import urllib.request
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

# カテゴリ別のコンテンツ生成プロンプト（プレーンテキスト形式）
CONTENT_PROMPTS = {
    "prompt": """あなたはAIプロンプトの専門家です。以下の商品情報に基づいて、実際に販売できるプロンプト集を作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. タイトルと目次
2. はじめに（使い方説明）
3. 各章に10個ずつのプロンプト（合計50個）
4. プロンプトは実際にコピペして使える形式で
5. 各プロンプトに「使い方のコツ」を1行追加

本文のみを出力してください。""",

    "ebook": """あなたはベストセラー作家です。以下の商品情報に基づいて、電子書籍のコンテンツを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. タイトルページ
2. 目次（5〜7章）
3. はじめに
4. 各章の本文（各章1000文字程度）
5. まとめ・あとがき

本文のみを出力してください。""",

    "checklist": """あなたは生産性向上の専門家です。以下の商品情報に基づいて、チェックリスト/ワークシートを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- チェック項目は「□」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. タイトルと概要
2. 使い方ガイド
3. メインチェックリスト（20〜30項目）
4. サブチェックリスト（カテゴリ別に3〜5セット）
5. 振り返りシート

本文のみを出力してください。""",

    "course": """あなたはオンライン講師です。以下の商品情報に基づいて、オンラインコースのカリキュラムと講義スクリプトを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. コース概要と学習目標
2. カリキュラム（5〜7モジュール）
3. 各モジュールの講義スクリプト（各1500文字程度）
4. 演習問題とワーク
5. まとめと次のステップ

本文のみを出力してください。""",

    "notion": """あなたはNotionテンプレートの専門家です。以下の商品情報に基づいて、Notionテンプレートの構成案と使い方ガイドを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要
2. データベース構成（プロパティ一覧、ビュー設定）
3. ページ構成（各ページの役割と使い方）
4. 使い方ガイド（ステップバイステップ）
5. カスタマイズのヒント
6. FAQ

本文のみを出力してください。""",

    "excel": """あなたはExcelの専門家です。以下の商品情報に基づいて、Excelテンプレートの構成案と使い方ガイドを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要
2. シート構成（各シートの役割）
3. 入力項目一覧と計算式の説明
4. 使い方ガイド（ステップバイステップ）
5. カスタマイズ方法
6. よくある質問

本文のみを出力してください。""",

    "spreadsheet": """あなたはGoogleスプレッドシートの専門家です。以下の商品情報に基づいて、スプレッドシートテンプレートの構成案と使い方ガイドを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要
2. シート構成（各シートの役割）
3. 入力項目一覧と計算式の説明
4. 使い方ガイド（ステップバイステップ）
5. カスタマイズ方法
6. よくある質問

本文のみを出力してください。""",

    "powerpoint": """あなたはプレゼンテーションの専門家です。以下の商品情報に基づいて、PowerPointテンプレートの構成案とスライド原稿を作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要とデザインコンセプト
2. スライド構成（各スライドの役割）
3. 各スライドの原稿テキスト
4. 使い方ガイド
5. カスタマイズのヒント

本文のみを出力してください。""",

    "canva": """あなたはCanvaデザインの専門家です。以下の商品情報に基づいて、Canvaテンプレートの構成案とデザインガイドを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要とデザインコンセプト
2. テンプレート構成（各デザインの用途）
3. カラーパレットとフォント設定
4. 使い方ガイド（Canvaでの編集方法）
5. カスタマイズのヒント
6. 活用例

本文のみを出力してください。""",

    "figma": """あなたはFigmaデザインの専門家です。以下の商品情報に基づいて、Figmaテンプレートの構成案とデザインシステムを作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. テンプレート概要とデザインコンセプト
2. コンポーネント構成
3. デザイントークン（色、タイポグラフィ、スペーシング）
4. 使い方ガイド
5. カスタマイズ方法

本文のみを出力してください。""",

    "linestamp": """あなたはLINEスタンプクリエイターです。以下の商品情報に基づいて、LINEスタンプのキャラクター設定とセリフ案を作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. スタンプセット概要
2. キャラクター設定（外見、性格、特徴）
3. スタンプ40個分のセリフ・表情一覧
4. 使用シーン例
5. 制作時の注意点

本文のみを出力してください。""",

    "icon": """あなたはアイコンデザイナーです。以下の商品情報に基づいて、アイコンセットのデザイン仕様書を作成してください。

【商品名】{product_name}
【ターゲット】{target}
{additional_notes}

【重要な出力ルール】
- 記号は使わないでください（#、*、**、-、```などは禁止）
- 見出しは「◆」や「■」を使ってください
- 箇条書きは「・」を使ってください
- 区切り線は「━━━━━━━━━━」を使ってください
- 読みやすい自然な日本語で書いてください

【構成】
1. アイコンセット概要とコンセプト
2. デザインスタイルガイド
3. アイコン50個分の一覧（名前と用途）
4. サイズバリエーション
5. 使用ガイドライン

本文のみを出力してください。""",
}


def generate_content_with_gemini(category: str, product_name: str, target: str, additional_notes: str = ""):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return generate_mock_content(category, product_name, target)

    base_prompt = CONTENT_PROMPTS.get(category, CONTENT_PROMPTS["prompt"])

    additional_text = f"【追加要望】{additional_notes}" if additional_notes else ""
    prompt = base_prompt.format(
        product_name=product_name,
        target=target,
        additional_notes=additional_text
    )

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 8192},
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["candidates"][0]["content"]["parts"][0]["text"]

            safe_name = product_name.replace(" ", "_").replace("/", "_")[:50]
            filename = f"{safe_name}.txt"

            return {"content": content, "filename": filename}
    except Exception as e:
        print(f"Gemini API error: {e}")
        return generate_mock_content(category, product_name, target)


def generate_mock_content(category: str, product_name: str, target: str):
    category_label = CATEGORY_LABELS.get(category, "デジタル商品")

    mock_content = f"""◆ {product_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ はじめに

この{category_label}は「{target}」の方に向けて作成しました。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 目次

・第1章：基本の使い方
・第2章：応用テクニック
・第3章：よくある質問

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 第1章：基本の使い方

ここに基本的な使い方の説明が入ります。

◇ ポイント1
・項目A
・項目B
・項目C

◇ ポイント2
・項目D
・項目E
・項目F

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 第2章：応用テクニック

応用的な使い方を紹介します。

◇ テクニック1
具体的な手順を説明...

◇ テクニック2
別のアプローチを説明...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ 第3章：よくある質問

Q: 〇〇はどうすればいいですか？
A: 〇〇の手順で対応できます。

Q: △△の場合はどうなりますか？
A: △△の場合は、□□を試してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ご購入ありがとうございました。
"""

    safe_name = product_name.replace(" ", "_").replace("/", "_")[:50]
    filename = f"{safe_name}.txt"

    return {"content": mock_content, "filename": filename}


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            category = data.get("category", "prompt")
            product_name = data.get("productName", "")
            target = data.get("target", "")
            additional_notes = data.get("additionalNotes", "")

            if not product_name:
                raise ValueError("productName is required")

            result = generate_content_with_gemini(category, product_name, target, additional_notes)

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

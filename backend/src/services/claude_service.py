import json
import anthropic
from src.config import settings
from src.types import GenerateRequest, GenerateResponse


CATEGORY_LABELS = {
    "prompt": "AIプロンプト集",
    "notion": "Notionテンプレート",
    "canva": "Canvaテンプレート",
    "ebook": "電子書籍",
}

PRICE_RANGES = {
    "prompt": (980, 2980),
    "notion": (500, 1500),
    "canva": (800, 2000),
    "ebook": (500, 1980),
}


async def generate_product(request: GenerateRequest) -> GenerateResponse:
    if not settings.anthropic_api_key:
        return _generate_mock_response(request)

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    category_label = CATEGORY_LABELS[request.category]
    price_min, price_max = PRICE_RANGES[request.category]

    prompt = f"""あなたはデジタル商品販売の専門家です。Gumroadで売れる商品を提案してください。

カテゴリ: {category_label}
ターゲット: {request.target}
{f"追加の要望: {request.additionalNotes}" if request.additionalNotes else ""}

以下の形式でJSON形式で出力してください（説明文は日本語で）:
{{
  "productNames": ["商品名1", "商品名2", "商品名3"],
  "description": "購買意欲を刺激する200-300文字の商品説明文",
  "suggestedPrice": {price_min}から{price_max}の間の価格（整数）,
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"]
}}

重要:
- 商品名はキャッチーで検索されやすいものにする
- 説明文は購入者のベネフィットを明確にする
- タグは検索で見つかりやすいキーワードを選ぶ
- JSONのみを出力し、他の説明は不要"""

    message = client.messages.create(
        model="claude-haiku-4-5-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text

    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        json_str = response_text[start:end]
        data = json.loads(json_str)
        return GenerateResponse(**data)
    except (json.JSONDecodeError, ValueError):
        return _generate_mock_response(request)


def _generate_mock_response(request: GenerateRequest) -> GenerateResponse:
    category_label = CATEGORY_LABELS[request.category]
    price_min, price_max = PRICE_RANGES[request.category]
    avg_price = (price_min + price_max) // 2

    return GenerateResponse(
        productNames=[
            f"【保存版】{request.target}のための{category_label}",
            f"{request.target}必見！即実践{category_label}",
            f"初心者OK！{request.target}向け{category_label}完全ガイド",
        ],
        description=f"「{request.target}」の方に向けた{category_label}です。\n\n"
        f"このテンプレートを使えば、面倒な作業を大幅に短縮できます。\n"
        f"初心者でもすぐに使い始められるよう、わかりやすい説明付き。\n\n"
        f"【含まれる内容】\n"
        f"・すぐに使えるテンプレート一式\n"
        f"・カスタマイズガイド\n"
        f"・活用事例集",
        suggestedPrice=avg_price,
        tags=[request.target, category_label, "テンプレート", "時短", "初心者向け"],
    )

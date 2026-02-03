from pydantic import BaseModel
from typing import Literal
from datetime import datetime


# 商品カテゴリ
ProductCategory = Literal[
    "prompt",       # AIプロンプト集
    "notion",       # Notionテンプレート
    "canva",        # Canvaテンプレート
    "ebook",        # 電子書籍
    "excel",        # Excelテンプレート
    "spreadsheet",  # スプレッドシート
    "powerpoint",   # PowerPointテンプレート
    "figma",        # Figmaテンプレート
    "checklist",    # チェックリスト/ワークシート
    "linestamp",    # LINEスタンプ
    "icon",         # アイコンセット
    "course",       # オンラインコース
]


# 商品生成リクエスト
class GenerateRequest(BaseModel):
    category: ProductCategory
    target: str
    additionalNotes: str | None = None


# 商品生成レスポンス
class GenerateResponse(BaseModel):
    productNames: list[str]
    description: str
    suggestedPrice: int
    tags: list[str]


# 設定
class SettingsRequest(BaseModel):
    gumroadToken: str
    monthlyGoal: int


# 売上データ
class Sale(BaseModel):
    id: str
    productName: str
    price: int
    saleTimestamp: datetime
    email: str


# 商品別売上
class ProductSales(BaseModel):
    productName: str
    count: int
    revenue: int


# 日別売上
class DailySales(BaseModel):
    date: str
    revenue: int


# ダッシュボードサマリー
class DashboardSummary(BaseModel):
    totalSales: int
    totalRevenue: int
    monthlyGoal: int
    salesByProduct: list[ProductSales]
    dailySales: list[DailySales]


# コンテンツ生成リクエスト
class GenerateContentRequest(BaseModel):
    category: ProductCategory
    productName: str
    target: str
    additionalNotes: str | None = None


# コンテンツ生成レスポンス
class GenerateContentResponse(BaseModel):
    content: str
    filename: str

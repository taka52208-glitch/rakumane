from pydantic import BaseModel
from typing import Literal
from datetime import datetime


# 商品カテゴリ
ProductCategory = Literal["prompt", "notion", "canva", "ebook"]


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

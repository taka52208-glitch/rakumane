from fastapi import APIRouter
from src.types import DashboardSummary, SettingsRequest
from src.services.gumroad_service import fetch_sales
from src.config import settings

router = APIRouter()

_user_settings = {
    "gumroad_token": "",
    "monthly_goal": 100000,
}


@router.get("/sales", response_model=DashboardSummary)
async def get_sales() -> DashboardSummary:
    token = _user_settings["gumroad_token"] or settings.gumroad_access_token
    return await fetch_sales(token, _user_settings["monthly_goal"])


@router.post("/settings")
async def save_settings(request: SettingsRequest) -> dict:
    _user_settings["gumroad_token"] = request.gumroadToken
    _user_settings["monthly_goal"] = request.monthlyGoal
    return {"status": "ok"}


@router.get("/settings")
async def get_settings() -> dict:
    return {
        "gumroadToken": "***" if _user_settings["gumroad_token"] else "",
        "monthlyGoal": _user_settings["monthly_goal"],
    }

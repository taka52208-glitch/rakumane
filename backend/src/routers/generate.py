from fastapi import APIRouter
from src.types import GenerateRequest, GenerateResponse
from src.services.claude_service import generate_product

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    return await generate_product(request)

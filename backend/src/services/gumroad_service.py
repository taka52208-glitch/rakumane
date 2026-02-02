from datetime import datetime, timedelta
from collections import defaultdict
import httpx
from src.types import DashboardSummary, ProductSales, DailySales


GUMROAD_API_BASE = "https://api.gumroad.com/v2"


async def fetch_sales(access_token: str, monthly_goal: int = 100000) -> DashboardSummary:
    if not access_token:
        return _generate_mock_dashboard(monthly_goal)

    async with httpx.AsyncClient() as client:
        today = datetime.now()
        first_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        response = await client.get(
            f"{GUMROAD_API_BASE}/sales",
            params={
                "access_token": access_token,
                "after": first_of_month.isoformat(),
            },
            timeout=30.0,
        )

        if response.status_code != 200:
            return _generate_mock_dashboard(monthly_goal)

        data = response.json()
        sales = data.get("sales", [])

        total_revenue = 0
        product_sales: dict[str, dict] = defaultdict(lambda: {"count": 0, "revenue": 0})
        daily_sales: dict[str, int] = defaultdict(int)

        for sale in sales:
            price = int(float(sale.get("price", 0)) * 100)
            product_name = sale.get("product_name", "Unknown")
            sale_date = sale.get("created_at", "")[:10]

            total_revenue += price
            product_sales[product_name]["count"] += 1
            product_sales[product_name]["revenue"] += price
            daily_sales[sale_date] += price

        sales_by_product = [
            ProductSales(productName=name, count=data["count"], revenue=data["revenue"])
            for name, data in sorted(
                product_sales.items(), key=lambda x: x[1]["revenue"], reverse=True
            )
        ]

        daily_sales_list = [
            DailySales(date=date, revenue=revenue)
            for date, revenue in sorted(daily_sales.items())
        ]

        return DashboardSummary(
            totalSales=len(sales),
            totalRevenue=total_revenue,
            monthlyGoal=monthly_goal,
            salesByProduct=sales_by_product,
            dailySales=daily_sales_list,
        )


def _generate_mock_dashboard(monthly_goal: int) -> DashboardSummary:
    today = datetime.now()
    daily_sales = []

    for i in range(14):
        date = today - timedelta(days=13 - i)
        revenue = 0
        daily_sales.append(DailySales(date=date.strftime("%Y-%m-%d"), revenue=revenue))

    return DashboardSummary(
        totalSales=0,
        totalRevenue=0,
        monthlyGoal=monthly_goal,
        salesByProduct=[],
        dailySales=daily_sales,
    )

from asyncio import sleep
from playwright.async_api import async_playwright
import json

from src.scraping.config import get_random_headers, PYAT_GET_STORE_URL, PYAT_GET_PRODUCT_URL, PYATOROCHKA_TYPES
from src.database.utils.enum_models import ProductTypes, MarketGroups
from src.database.orm import AsyncProductOrm

def data_generation(store_id: int, product_type: ProductTypes, row_data: dict):
        data = []
        for item in row_data:
             data.append(
                  {
                    "shop_id": store_id,
                    "product_type": product_type,
                    "name": item["name"],
                    "price": int(str(item["prices"]["regular"]).replace('.', '')),
                    "discount": round(1-(float(item["prices"]["discount"])/float(item["prices"]["regular"])), 2)*100 if item["prices"].get("discount") is not None else 0
                  }
             )
        return data

async def get_store(lat: float, long: float):
    data = dict()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        head = get_random_headers()
        context = await browser.new_context(
            user_agent=head[0],
            extra_http_headers=head[1],
            )

        page = await context.new_page()

        url = PYAT_GET_STORE_URL.format(long, lat)
        response = await page.goto(url)
        raw = await response.text()

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print("❌ Не удалось распарсить JSON")
        
        await browser.close()
        return data

async def get_data(store_id: int, store_code: str):
    data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for product_type, code_arr in PYATOROCHKA_TYPES.items():
            for code in code_arr:
                await sleep(3)
                head = get_random_headers()
                context = await browser.new_context(
                user_agent=head[0],
                extra_http_headers=head[1],
                )
                page = await context.new_page()

                url = PYAT_GET_PRODUCT_URL.format(store_code, code)
                response = await page.goto(url)
                raw = await response.text()
                try:
                    new_data = json.loads(raw)["products"]
                    for item in data_generation(store_id, product_type, new_data): data.append(item)
                    await AsyncProductOrm.add_products(data)
                    data = []
                except json.JSONDecodeError:
                    print("❌ Не удалось распарсить JSON")
                await page.close()
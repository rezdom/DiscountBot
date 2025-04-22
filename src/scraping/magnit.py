from httpx import AsyncClient
from geopy.distance import geodesic

from src.scraping.config import payloads, MAGNIT_URL_API, MAGNIT_GET_STORES_URL, MAGNIT_MAP_PAYLOAD
from src.database.utils.enum_models import ProductTypes
from src.database.orm import AsyncProductOrm
from src.scraping.geo import get_map_box

def data_generation(store_id: int, product_type: ProductTypes,row_data: dict):
        data = []
        for item in row_data:
             data.append(
                  {
                    "shop_id": store_id,
                    "product_type": product_type,
                    "name": item["name"],
                    "price": item["promotion"]["oldPrice"] if item["promotion"].get("oldPrice") is not None else item["price"],
                    "discount": item["promotion"]["discountPercent"] if item["promotion"].get("discountPercent") is not None else 0
                  }
             )
        return data

async def get_stores(lat: float, long: float, url: str = MAGNIT_GET_STORES_URL):
    data = []
    new_payload = MAGNIT_MAP_PAYLOAD
    res = get_map_box(lat, long)
    new_payload["geoBoundingBox"]["leftTopLatitude"] = res["leftTopLatitude"]
    new_payload["geoBoundingBox"]["leftTopLongitude"] = res["leftTopLongitude"]
    new_payload["geoBoundingBox"]["rightBottomLatitude"] = res["rightBottomLatitude"]
    new_payload["geoBoundingBox"]["rightBottomLongitude"] = res["rightBottomLongitude"]
    async with AsyncClient() as client:
        response = await client.post(url, json=new_payload)
        if response.status_code == 200:
            raw_stores = response.json()["stores"]
            data = [(item["address"], item["code"], round(geodesic((lat, long), (item["coordinates"]["latitude"], item["coordinates"]["longitude"])).kilometers, 3)) for item in raw_stores]    
        else:
            print(f"get_stores Error: {response.status_code}")
    sorted_data = sorted(data, key=lambda x: x[1])
    return sorted_data[:3]

async def get_data(store_id: int ,store_code: str, url: str = MAGNIT_URL_API):
    data = []
    async with AsyncClient() as client:
        for payload, product_type in payloads(store_code):
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                for item in data_generation(store_id, product_type, response.json()["items"]): data.append(item)
                await AsyncProductOrm.add_products(data)
                data = []
            else:
                print(f"get_stores Error: {response.status_code}")
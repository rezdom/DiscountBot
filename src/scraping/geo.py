from geopy.geocoders import Nominatim
from asyncio import run, to_thread

async def get_address_info(address: str):
    geolocator = Nominatim(user_agent="discount_bot")
    location = await to_thread(geolocator.geocode, address)
    return location

def get_map_box(latitude: float, longitude: float):
    height = 0.06
    width = 0.12

    return {
        "leftTopLatitude": latitude + height / 2,
        "leftTopLongitude": longitude - width / 2,
        "rightBottomLatitude": latitude - height / 2,
        "rightBottomLongitude": longitude + width / 2,
    }

async def main():
    location = await get_address_info("Бугульма улица Сосновая,  2")
    print(location)

if __name__ == "__main__":
    run(main())
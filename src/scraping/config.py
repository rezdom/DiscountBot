from src.database.utils.enum_models import ProductTypes
import time

MAGNIT_URL_API = "https://magnit.ru/webgate/v2/goods/search"
MAGNIT_GET_STORES_URL = "https://magnit.ru/webgate/v1/store-search/geo"
PYAT_GET_STORE_URL = "https://5d.5ka.ru/api/orders/v1/orders/stores/?lon={}&lat={}"
PYAT_GET_PRODUCT_URL = "https://5d.5ka.ru/api/catalog/v2/stores/{}/categories/{}/products?mode=delivery&include_restrict=true&limit=499"

MAGNIT_PRODUCT_PAYLOAD = {
    "sort": {
        "order": "desc",
        "type": "popularity"
    },
    "pagination": {
        "limit": 50,
        "offset": 0
    },
    "categories": None,
    "includeAdultGoods": True,
    "storeCode": None,
    "storeType": "1",
    "catalogType": "1"
}

MAGNIT_MAP_PAYLOAD = {
    "aggs": False,
    "geoBoundingBox": {
        "leftTopLatitude": None,
        "leftTopLongitude": None,
        "rightBottomLatitude": None,
        "rightBottomLongitude": None
    },
    "limit": 5000,
    "storeTypes": [
        1,
        2,
        6,
        5
    ]
}

import random

USER_AGENTS = [
    # Chrome (Windows/Mac/Linux)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    
    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/119.0',
    
    # Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    
    # Mobile (Android/iOS)
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    
    # Advanced
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Vivaldi/6.2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
    
    # Old version
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    
    # Linux/non standart
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def get_random_headers():
    return random.choice(USER_AGENTS), {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en;q=0.9",
        "origin": "https://5ka.ru",
        "referer": "https://5ka.ru/",
        "x-app-version": "0.1.1.dev",
        "x-device-id": "30ae88e7-193c-4e6e-af3e-c74864261bce",
        "x-platform": "webapp",
    }

MAGNIT_TYPES = {
    ProductTypes.ALCO: [
        [47161, 41179, 41185, 41187, 41189, 41191, 41193, 41195, 41197, 41199, 41201, 41203,
             47261, 47263, 47265, 47267, 41183, 23293, 41207, 41209, 41211, 47269],
    ],
    ProductTypes.OTHER: [
        [4435, 53281 ,53299 ,53303 ,53309 ,53311 ,53315 ,53317 ,53323 ,45355 ,53283],
        [16363, 16369, 16393, 16399, 16403, 16401, 16375, 38985, 16371, 38973,
         38975, 38979, 38991, 38999, 39011, 16365, 18739, 16381, 16387, 16373, 16389],
        [4459, 4467, 45505, 45507, 45509, 38553, 4463, 4464, 18615, 45495, 45497,
         18477, 18485, 18483, 18493, 18489, 18487, 38395, 4460, 4461],
        [7485, 35731, 35725, 35729, 7505,
         46011, 35735, 7504, 7503, 17483, 57387, 35727, 7502, 7501,
         7507, 7498, 7508, 55701, 44885, 45071, 45073, 45075, 45077,
         45067, 45069, 44909, 45111, 45119, 45113, 45115, 45121, 60729],
        [7660, 28005, 28009, 28011, 28015, 28019, 28035, 28031, 39373,
         39375, 39377, 7775, 27987, 27989, 11953, 28001, 41961, 41967, 41969],
        [4488, 16551, 16561, 16563, 16565, 45775, 47739,
         16553, 16583, 16581, 16585, 45779, 61361],
        [ 44547, 44597, 44599, 44603, 44607, 44605, 44601, 44611, 44977, 44983, 44985, 44989, 44987,
         44979, 44981, 44549, 44575, 44579, 44573, 44577, 44551, 44581],
    ],
    ProductTypes.DAIRY_EGGS: [
        [ 4834, 26995,45723, 45725, 18061, 45727, 4843, 4840, 17637, 17639, 4854, 4838,
         4844, 45717, 45715, 45719, 4837, 4842, 18063, 27187, 4835, 38633, 38637, 17629, 45757, 17625, 4845, 38547,
         17673, 17621, 57385, 4839, 45751, 45753, 17487, 17493, 17491, 17489, 17495, 45761, 58909, 61357, 61391],
         [37741, 4847, 57745, 4848, 4849, 4851, 38037],
    ],
    ProductTypes.VEGETABLES_FRUITS: [
        [4884, 45763, 45771, 45769, 45767, 45773, 4894, 4887,
         45789, 45791, 45795, 4885, 45797, 4886, 45801, 45803, 45805, 16737, 45793, 60791, 60793, 60795],
    ],
    ProductTypes.BAKERY: [
        [5269, 5270, 5274, 53363, 53365, 18123, 18437, 17129, 18337, 53347, 53339,
         53349, 53333, 53335, 53331, 55755, 53367],
    ],
    ProductTypes.GROCERY_SAUCES: [
        [4528, 4547, 44595, 16533, 4551, 16531, 16461, 4548, 45359,
         47357, 4563, 4565, 4566, 4567, 16349, 16355, 56345, 4534, 38917, 38915, 38919,
         4556, 4560, 4558, 4561, 44045, 4562, 38845, 45109, 4537, 4538, 4541, 16535, 16537],
    ],
    ProductTypes.MEAT: [
        [4855, 4866, 38051, 38053, 45971, 38187, 38061, 45973, 4867,
         45919, 4868, 4857, 38189, 17979, 45915, 45917],
         [17591, 38567, 17607, 46109, 46113, 4869, 38569,
          4859, 4862, 38575, 4861, 4863, 4871, 38571],
    ],
    ProductTypes.FISH: [
        [4998, 38559, 26739, 26741, 7361, 5010, 5002,
         5009, 4999, 38287, 5001, 5006, 5007, 5008, 5003],
    ],
    ProductTypes.SWEETS: [
        [5011, 7197, 7202, 7216, 7199, 7218, 7201, 50675, 61079, 16979, 7203, 7214, 7204, 7209, 7207,
         35737, 5013, 7220, 7222, 7217, 7365, 5012, 7219, 7221, 7223],
    ],
    ProductTypes.TEA_COFFEE: [
        [5276, 5280, 38945, 38943, 38951, 38949, 38953, 5279,
         44121, 12787, 12783, 12785, 12791, 46641, 38731, 44593, 16181],
    ],
    ProductTypes.DRINKS: [
        [4874, 7157, 39107, 39117, 39111, 39113, 39115, 4875, 39145, 39147,
         39149, 39151, 26777, 26877, 4882, 4876, 7764, 4883, 39031, 60873],
    ],
    ProductTypes.SNACKS_NUTS: [
        [12435, 12437, 45983, 45981, 45985, 45987, 45989, 55165, 44119, 12541,
         12439, 12697, 12547, 12441, 16143, 16145, 16149, 16147, 38661],
    ],
    ProductTypes.CHEMISTRY: [
        [28475, 44665, 44669, 44675, 44673, 44679, 44681, 44683, 44677, 44671, 44975, 45063, 45065, 44685, 40307, 40337,
         40311, 40303, 40309, 40299, 46105, 40341, 51043, 60213, 61157, 46047, 40301, 40305, 61073, 61349],
    ]
}

PYATOROCHKA_TYPES = {
    ProductTypes.OTHER: ["251C12884", "251C12903", "251C12905", "251C12906", "251C12907", "251C12910"],
    ProductTypes.VEGETABLES_FRUITS: ["251C12886", ],
    ProductTypes.DAIRY_EGGS: ["251C12887", ],
    ProductTypes.BAKERY: ["251C12888", ],
    ProductTypes.MEAT: ["251C12889", ],
    ProductTypes.FISH: ["251C12890", ],
    ProductTypes.SWEETS: ["251C12900", ],
    ProductTypes.SNACKS_NUTS: ["251C12901", ],
    ProductTypes.GROCERY_SAUCES: ["251C12902", ],
    ProductTypes.DRINKS: ["251C12904", ],
    ProductTypes.CHEMISTRY: ["251C12908", "251C12909", ],
    ProductTypes.ALCO: ["251C13047", ],
    ProductTypes.TEA_COFFEE: ["251C13057", ]
}

def payloads(store_code: str, new_payload: dict = MAGNIT_PRODUCT_PAYLOAD):
    new_payload["storeCode"] = store_code
    for product_type, arr_type in MAGNIT_TYPES.items():
        for item in arr_type:
            new_payload["categories"] = item
            yield new_payload, product_type
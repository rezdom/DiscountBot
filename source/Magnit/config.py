class ActualError(Exception):
    def __init__(self, errmsg, city_table_name) -> None:
        self.errmsg = errmsg
        self.city_table_name = city_table_name

class FindCityError(Exception):
    def __init__(self, errmsg) -> None:
        self.errmsg = errmsg     

headers_for_magnit = {
    "accept": "*/*",
    "accept-language": "ru,ru-RU;q=0.9,en-RU;q=0.8,en-US;q=0.7,en;q=0.6",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-app-version": "0.1.0",
    "x-client-name": "magnit",
    "x-device-id": "ie5h31ju1n",
    "x-device-platform": "Web",
    "x-device-tag": "disabled",
    "x-platform-version": "window.navigator.userAgent",
    "Referer": "https://magnit.ru/",
    "Referrer-Policy": "origin"
  }

file_path = [
    r"source\Magnit\cities_info.db",
    r"source\Magnit\stores_info.db",
    r"source\Magnit\products_json\cards_info.db",
    r"source\Magnit\products_json\\"
]

TOKEN_API = "6128370261:AAETFUgFmkK_L_b-v8Y2k9bLc1UTY0Ouj_U"

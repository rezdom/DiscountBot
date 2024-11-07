import requests, json, os, math
import sys, sqlite3
sys.path.append(os.path.abspath('../BotParsSale'))
from source.Magnit import config
from datetime import datetime
import uuid



class ScrapyMagnitBot:

    def __init__(self, latitude, longitude):
        
        self.latitude = latitude
        self.longitude = longitude
        self.db_for_cities = sqlite3.connect(config.file_path[0])
        self.cur_for_cities = self.db_for_cities.cursor()
        self.db_for_stores = sqlite3.connect(config.file_path[1])
        self.cur_for_stores = self.db_for_stores.cursor()
        self.db_for_cards = sqlite3.connect(config.file_path[2])
        self.cur_for_cards = self.db_for_cards.cursor()
    


    def create_city_table(self, city, instance):
        
        instance.cur_for_cities.execute(f"CREATE TABLE IF NOT EXISTS {city}(date TEXT, adress TEXT, longitude REAL, latitude REAL, shopID INTEGER)")       
        instance.db_for_cities.commit()




    def create_store_info(self, storeID, address, db, cur):

        cur.execute(f"CREATE TABLE IF NOT EXISTS store{storeID}(date TEXT, adress TEXT, fileID TEXT)")

        response = requests.get(f"https://web-gateway.middle-api.magnit.ru/v1/promotions?offset=0&limit=20&storeId={storeID}&sortBy=priority&order=desc&adult=true",
                                     headers=config.headers_for_magnit)
        cards_limit = response.json()['total']
        response = requests.get(f"https://web-gateway.middle-api.magnit.ru/v1/promotions?offset=0&limit={cards_limit}&storeId={storeID}&sortBy=priority&order=desc&adult=true",
                                     headers=config.headers_for_magnit)
        
        ID = str(uuid.uuid4())
        json_products = response.json()['data']

        cur.execute(f"INSERT INTO store{storeID} VALUES (?, ?, ?)",(datetime.now().date(), address, ID))
        db.commit()

        with open(f"{config.file_path[3]}{ID}.json", 'w', encoding='utf-8') as file:
            json.dump(json_products, file, ensure_ascii=False, indent=4)
        return ID


    async def for_filter(self, fileID, db, cur):
        cur.execute(f"CREATE TABLE IF NOT EXISTS id_{fileID.split('-')[0]}(other TEXT, bakal_souse TEXT, konditer TEXT, him TEXT, water TEXT, tea_coffe TEXT, freeze TEXT, milk_eggs TEXT, meat TEXT, fish TEXT, fruts_veg TEXT, discount INTEGER)")
        with open(f'{config.file_path[3]}{fileID}.json', 'r', encoding='utf-8') as file:
            json_obj = json.load(file)
            for card in json_obj:
                    if "discountPercentage" not in card:
                        discount = f"-0%"
                        oldprice = f"<strike>without discount</strike>"
                        nowprice = f"<b>этот тавар находиться в акции{card['description']}</b>"
                    else: 
                        discount = f"-{card['discountPercentage']}%"
                        if "oldPrice" in card:
                            oldprice = f"<strike>{str(card['oldPrice'])[:-2]},{str(card['oldPrice'])[-2:]}₽</strike>"
                            nowprice = f"<b>{str(card['price'])[:-2]},{str(card['price'])[-2:]}₽</b>"
                        else:
                            oldprice = f"<strike>oldprice not found</strike>"
                            nowprice = f"<b>nowprice not found</b>"
                    name = card['name']

                    if card['categoryName'] == "Бакалея, соусы":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(bakal_souse, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Кондитерские изделия":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(konditer, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Бытовая химия":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(him, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))

                    elif card['categoryName'] == "Напитки":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(water, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Чай, кофе, какао":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(tea_coffe, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Замороженные продукты":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(freeze, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Молоко, сыр, яйца":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(milk_eggs, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Мясо, птица, колбасы":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(meat, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Рыба и морепродукты":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(fish, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    elif card['categoryName'] == "Овощи и фрукты":
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(fruts_veg, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
                            
                    else:
                        cur.execute(f"INSERT INTO id_{fileID.split('-')[0]}(other, discount) VALUES (?, ?)",(f"{name}\n{discount}\n{oldprice}\n{nowprice}", discount[1:3] if len(discount) == 4 else discount[1:2]))
        db.commit()
        return fileID.split('-')[0]



    def get_key(self, d, value):
        for k, v in d.items():
            if v == value:
                return k, v


    def find_minimal_distance(self, arr, latitude, longitude, instance):
        memory = {}
        x_list = []
        result = []
        for item in arr:
            d = math.acos(math.sin(math.radians(latitude))*math.sin(math.radians(item[0])) + math.cos(math.radians(latitude))*math.cos(math.radians(item[0]))*math.cos(abs(math.radians(longitude) - math.radians(item[1]))))
            L = d*6371
            memory[(item[0],item[1])] = L, item[2]
            x_list.append((L,item[2]))
        x_list.sort()
        for item in x_list[0:3]:
            result.append(instance.get_key(memory, item))
        return result


    def get_address_from_crd(self, latitude, longitude):
    #заполняем параметры, которые описывались выже. Впиши в поле apikey свой токен!
        PARAMS = {
            "apikey":"56149620-f193-4e6e-9ad8-eb1e9003214d",
            "geocode": f"{longitude},{latitude}",
            "format":"json",
            "lang":"ru_RU"
        }
        #отправляем запрос по адресу геокодера.
        try:
            r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
            #получаем данные
            r.content.decode('utf-8')
            json_data = r.json()
            #вытаскиваем из всего пришедшего json именно строку с полным адресом.
            address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
            #возвращаем полученный адрес
            addrss_arr = address_str.split(', ')
            memory = []
            for item in addrss_arr:
                if 'посёлок'  in item:
                    memory.append(item.split(' ')[-1]); break
                elif 'городского типа' in item:
                    memory.append(item.split(' ')[-1]); break
                elif 'деревня' in item:
                    memory.append(item.split(' ')[-1]); break
                elif 'сельское поселение' in item:
                    memory.append(item.split(' ')[-1]); break
            if memory == []:
                memory.append((address_str.split(', ')[1] if len(address_str.split(', ')[1].split(' ')) == 1 else address_str.split(', ')[2]))
            for item in addrss_arr:
                if 'край' in item:
                    memory.append(item); break
                elif 'область' in item:
                    memory.append(item); break
                elif 'Республика' in item:
                    memory.append(item); break
                elif 'округ' in item:
                    memory.append(item); break
            return(memory)
        except Exception as e:
            #если не смогли, то возвращаем ошибку
            return "error"
    
    
    def find_city(self, city, region, instance):
       
        response = requests.get(f"https://web-gateway.middle-api.magnit.ru/v1/cities?query={city}", headers=config.headers_for_magnit)
        if response.json()['total'] == 0:
            raise config.FindCityError("такого города нет в поиске магнита")
        elif response.json()['total'] == 1:
            instance.cur_for_cities.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{city}'")
            if len(instance.cur_for_cities.fetchall()) == 0:
                instance.create_city_table(city, instance)
                return city, response.json()['cities'][0]['latitude'], response.json()['cities'][0]['longitude']
            else:
                instance.cur_for_cities.execute(f"SELECT date FROM {city}")
                if ((datetime.now().date() - datetime.strptime(instance.cur_for_cities.fetchone()[0], '%Y-%m-%d').date()).days > 15):
                    instance.cur_for_cities.execute(f"DROP TABLE IF EXISTS {city}")
                    instance.create_city_table(city, instance)
                    return city, response.json()['cities'][0]['latitude'], response.json()['cities'][0]['longitude']
                else:
                    raise config.ActualError("ошибка | актуальный файл | город", city)
        else:
            memory = None
            for item in response.json()['cities']:
                if item['region'] == region:
                    city = f"{city}_{region.replace(' ', '_')}"
                    memory = item
                    break
            if memory == None:
                raise config.FindCityError("такого города нет в поиске магнита")
            instance.cur_for_cities.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{city}'")
            if len(instance.cur_for_cities.fetchall()) == 0:
                instance.create_city_table(city, instance)
                return city, memory['latitude'], memory['longitude']
            else:
                instance.cur_for_cities.execute(f"SELECT date FROM {city}")
                if ((datetime.now().date() - datetime.strptime(instance.cur_for_cities.fetchone()[0], '%Y-%m-%d').date()).days > 15):
                    instance.cur_for_cities.execute(f"DROP TABLE IF EXISTS {city}")
                    instance.create_city_table(city, instance)
                    return city, memory['latitude'], memory['longitude']
                else:
                    raise config.ActualError("ошибка | актуальный файл | город_регион", city)

    def find_big_city(self, city, instance):
       
        response = requests.get(f"https://web-gateway.middle-api.magnit.ru/v1/cities?query={city}", headers=config.headers_for_magnit)
        if response.json()['total'] == 0:
            raise config.FindCityError("такого города нет в поиске магнита")
        else:
            instance.cur_for_cities.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{city}'")
            if len(instance.cur_for_cities.fetchall()) == 0:
                instance.create_city_table(city, instance)
                return city, response.json()['cities'][0]['latitude'], response.json()['cities'][0]['longitude']
            else:
                instance.cur_for_cities.execute(f"SELECT date FROM {city}")
                if ((datetime.now().date() - datetime.strptime(instance.cur_for_cities.fetchone()[0], '%Y-%m-%d').date()).days > 15):
                    instance.cur_for_cities.execute(f"DROP TABLE IF EXISTS {city}")
                    instance.create_city_table(city, instance)
                    return city, response.json()['cities'][0]['latitude'], response.json()['cities'][0]['longitude']
                else:
                    raise config.ActualError("ошибка | актуальный файл | город", city)
                

    def input_cities_table(self, city, latitude, longitude, instance):
        

        response = requests.get(f"https://web-gateway.middle-api.magnit.ru/v1/geolocation/store?Longitude={longitude}&Latitude={latitude}&Radius=30&Limit=1500",
                                headers=config.headers_for_magnit)
        
        city_one_name = city if '_' not in city else city.split('_')[0]
        for store in response.json()['stores']:
            city_store = store['address'].split(' ')[0:2]         
            if city_one_name in city_store and (store['type'] == "1" or store['type'] == "2"):
                instance.cur_for_cities.execute(f"INSERT INTO {city} VALUES (?, ?, ?, ?, ?)",(datetime.now().date(), store['address'], store['longitude'], store['latitude'], store['id']))
        instance.db_for_cities.commit()

    
    def find_nearest_store(self, city, latitude, longitude,instance): #находим ближайшие магазины

        instance.cur_for_cities.execute(f"SELECT latitude, longitude, adress FROM {city}")
        strores_coordinations = instance.cur_for_cities.fetchall()

        minimal_distance = instance.find_minimal_distance(strores_coordinations,latitude,longitude,instance)   
        return minimal_distance

    

    async def get_product_cards(self, storeID, address, instance):
        instance.cur_for_stores.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='store{storeID}'")
        if len(instance.cur_for_stores.fetchall()) == 0:
            ID = instance.create_store_info(storeID, address, instance.db_for_stores, instance.cur_for_stores)
            await instance.for_filter(ID, instance.db_for_cards, instance.cur_for_cards)
            return ID.split('-')[0]
        else:
            instance.cur_for_stores.execute(f"SELECT date FROM store{storeID}")
            if datetime.strptime(instance.cur_for_stores.fetchone()[0], '%Y-%m-%d').date() != datetime.now().date():
                instance.cur_for_stores.execute(f"SELECT fileID FROM store{storeID}")              
                fileID_for_del = instance.cur_for_stores.fetchone()[0]
                os.remove(f"{config.file_path[3]}{fileID_for_del}.json")
                instance.cur_for_cards.execute(f"DROP TABLE IF EXISTS id_{fileID_for_del.split('-')[0]}")
                instance.cur_for_stores.execute(f"DROP TABLE IF EXISTS store{storeID}")
                ID = instance.create_store_info(storeID, address, instance.db_for_stores, instance.cur_for_stores)
                await instance.for_filter(ID, instance.db_for_cards, instance.cur_for_cards)
                return ID.split('-')[0]
            else:
                instance.cur_for_stores.execute(f"SELECT fileID FROM store{storeID}")
                print('файл актуален')
                return instance.cur_for_stores.fetchone()[0].split('-')[0]



    def selected_city(self, tup_coord, city, instance):
        
        instance.cur_for_cities.execute(f"SELECT shopID FROM {city} WHERE latitude == {float(tup_coord[0])}")
        shopID = int(instance.cur_for_cities.fetchone()[0])
        instance.cur_for_cities.execute(f"SELECT adress FROM {city} WHERE latitude == {float(tup_coord[0])}")
        address = instance.cur_for_cities.fetchone()[0]
        return shopID, address
    


class ScrapyMagnitBot_HandMode(ScrapyMagnitBot):

    def __init__(self, address):
        self.address = address
        self.db_for_cities = sqlite3.connect(config.file_path[0])
        self.cur_for_cities = self.db_for_cities.cursor()
        self.db_for_stores = sqlite3.connect(config.file_path[1])
        self.cur_for_stores = self.db_for_stores.cursor()
        self.db_for_cards = sqlite3.connect(config.file_path[2])
        self.cur_for_cards = self.db_for_cards.cursor()
    
    def get_crd_from_address(self, address):
        PARAMS = {
            "apikey":"56149620-f193-4e6e-9ad8-eb1e9003214d",
            "geocode": f"{'+'.join(address.split(' '))}",
            "format":"json",
            "lang":"ru_RU"
        }
        try:
            r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
            r.content.decode('utf-8')
            json_data = r.json()
            coordination_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            coordination = coordination_str.split(' ')
            return coordination
        except Exception as e:
            return "error" 

        



            
        


if __name__ == '__main__':
    #тесты
    bot = ScrapyMagnitBot(54.539939,52.830721)
    try:
        coordinations = bot.get_address_from_crd(bot.latitude,bot.longitude)
        current_city = bot.find_city(coordinations[0],coordinations[1])
        bot.input_cities_table(current_city[0],current_city[1],current_city[2],bot)
        minimal_distance = bot.find_nearest_store(current_city[0],bot.latitude,bot.longitude)
        store_coordinations = tuple(input('введи координаты понравившегося магазина:').split(', '))
        storeID, address = bot.selected_city(store_coordinations,current_city[0],bot)
        print(storeID)
    except config.FindCityError:
        print('Город не найден')
    except config.ActualError as ae:
        print('Информация актуальна')
        minimal_distance = bot.find_nearest_store(ae.args[1],bot.latitude,bot.longitude)
        store_coordinations = tuple(input('введи координаты понравившегося магазина:').split(', '))
        storeID, address = bot.selected_city(store_coordinations,ae.args[1],bot)
        print(storeID)
    
    fileID_cut = bot.get_product_cards(storeID, address)
    print(fileID_cut)

import requests, json, os, math
import sys, sqlite3
sys.path.append(os.path.abspath('../BotParsSale'))
from source.Pyatorochka import config_pyat
from datetime import datetime
import aiohttp


class ScrapyPyatBot:

    def __init__(self, latitude, longitude) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.db_for_cards = sqlite3.connect(config_pyat.file_path[0])
        self.cur_for_cards = self.db_for_cards.cursor()

    def card_filter(self, card, code, db, cur):
        self.cur_for_cards.execute(f"CREATE TABLE IF NOT EXISTS id{code}(date TEXT,other TEXT, bakal_souse TEXT, konditer TEXT, him TEXT, water TEXT, tea_coffe TEXT, freeze TEXT, milk_eggs TEXT, meat TEXT, fish TEXT, fruts_veg TEXT, discount INTEGER)")
        discount = round((1-round((card['current_prices']['price_promo__min']/card['current_prices']['price_reg__min']),2))*100)
        discount = f"-{discount}%"
        name = card['name']
        oldprice = f"<strike>{card['current_prices']['price_reg__min']}₽</strike>"
        nowprice = f"<b>{card['current_prices']['price_promo__min']}₽</b>"
        mech = f"Условие:{card['mech']}"

        if 'макарон' in card['name'].lower() or 'крупа' in card['name'].lower() or 'приправа' in card['name'].lower() or 'подсолнечно' in card['name'].lower() or 'хлопья' in card['name'].lower() or 'рис' in card['name'].lower() or 'соус' in card['name'].lower() or 'майонез' in card['name'].lower() or 'мука' in card['name'].lower() or 'кетчуп' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,bakal_souse, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,bakal_souse, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))  
                            
        elif 'торт' in card['name'].lower() or 'конфет' in card['name'].lower() or 'десерт' in card['name'].lower() or 'ирис' in card['name'].lower() or 'батончик' in card['name'].lower() or 'мармелад' in card['name'].lower() or 'мороженое' in card['name'].lower() or 'вафли' in card['name'].lower() or 'печенье' in card['name'].lower() or 'пудинг' in card['name'].lower() or 'макарон' in card['name'].lower() or 'шоколад' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,konditer, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,konditer, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))  
                            
        elif 'крем-краска' in card['name'].lower() or 'ласка' in card['name'].lower() or 'domestos' in card['name'].lower() or 'засор' in card['name'].lower() or 'чистки' in card['name'].lower() or 'мытья' in card['name'].lower() or 'стиральный' in card['name'].lower() or 'пятновывод' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,him, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,him, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
                        
        elif 'вода' in card['name'].lower() or 'нектар' in card['name'].lower() or 'сок' in card['name'].lower() or 'квас' in card['name'].lower() or 'напиток' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,water, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,water, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))    
                            
        elif 'чай' in card['name'].lower() or 'кофе' in card['name'].lower() or 'суаре' in card['name'].lower() or 'цикорий' in card['name'].lower() or 'какао' in card['name'].lower() or 'вода' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,tea_coffe, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,tea_coffe, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))  
                            
        elif 'блин' in card['name'].lower() or 'котлет' in card['name'].lower() or 'чебуп' in card['name'].lower() or 'пельм' in card['name'].lower() or 'вареник' in card['name'].lower() or 'полуфабрикй' in card['name'].lower() or 'фарширов' in card['name'].lower() or 'пицца' in card['name'].lower() or 'наггет' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,freeze, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:           
                cur.execute(f"INSERT INTO id{code} (date ,freeze, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            
        elif 'творо' in card['name'].lower() or 'катык' in card['name'].lower() or 'молоко' in card['name'].lower() or 'кефир' in card['name'].lower() or 'сметана' in card['name'].lower() or 'сырок' in card['name'].lower() or 'простокваша' in card['name'].lower() or 'сыр' in card['name'].lower() or 'йогурт' in card['name'].lower() or 'сливоч' in card['name'].lower() or 'яйца' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,milk_eggs, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,milk_eggs, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
                            
        elif 'мясо' in card['name'].lower() or 'сардель' in card['name'].lower() or 'сосис' in card['name'].lower() or 'колбас' in card['name'].lower() or 'груд' in card['name'].lower() or 'шашлык' in card['name'].lower() or 'паштет' in card['name'].lower() or 'птиц' in card['name'].lower() or 'стейк' in card['name'].lower() or 'фарш' in card['name'].lower() or 'творо' in card['name'].lower() or 'свин' in card['name'].lower() or 'говя' in card['name'].lower() or 'курица' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,meat, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,meat, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
                            
        elif 'шпрот' in card['name'].lower() or 'тунец' in card['name'].lower() or 'сардин' in card['name'].lower() or 'килька' in card['name'].lower() or 'сайра' in card['name'].lower() or 'кальмар' in card['name'].lower() or 'скумбр' in card['name'].lower() or 'сельдь' in card['name'].lower() or 'мясо' in card['name'].lower() or 'креветк' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,fish, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,fish, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
                            
        elif 'грибы' in card['name'].lower() or 'чипсы' in card['name'].lower() or 'зелень' in card['name'].lower() or 'овощ' in card['name'].lower() or 'фасоль' in card['name'].lower() or 'горошек' in card['name'].lower() or 'шампин' in card['name'].lower() or 'томат' in card['name'].lower() or 'оливки' in card['name'].lower() or 'огурц' in card['name'].lower() or 'изюм' in card['name'].lower() or 'яблоки' in card['name'].lower() or 'фрукт' in card['name'].lower():
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,fruts_veg, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,fruts_veg, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
                            
        else:
            if card['mech'] == None:
                cur.execute(f"INSERT INTO id{code} (date ,other, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))
            else:
                cur.execute(f"INSERT INTO id{code} (date ,other, discount) VALUES (?,?,?)",(datetime.now().date(),f"{name}\n{discount}\n{oldprice}\n{nowprice}\n{mech}", int(discount[1:3]) if len(discount) == 4 else int(discount[1:2])))

        db.commit()
    
    async def get_stores(self, latitude, longitude):
        async with aiohttp.ClientSession() as session:
            next_page=(f"https://5ka.ru/api/v3/stores/?lat={latitude}&lon={longitude}&radius=20000")
            distance_arr = []
            memory = {}
            result = []
            while next_page != None:
                async with session.get(url=next_page) as response:
                    json_file = await response.json()
                    if json_file['results'] == []:
                        raise config_pyat.FindCityError
                    for item in json_file['results']:
                        distance_arr.append(item['distance']/1000)
                        memory[item['distance']/1000] = (item['address'],item['sap_code'],item['lat'],item['lon'])
                    next_page = json_file['next']
            
            for i in range(len(distance_arr)-1):
                for j in range(len(distance_arr)-1-i):
                    if distance_arr[j] > distance_arr[j+1]:
                        distance_arr[j],distance_arr[j+1] = distance_arr[j+1],distance_arr[j]
            distance_arr = distance_arr[0:3]
            
            for k in list(memory):
                for i in distance_arr:
                    if i == k:
                        result.append((k,memory.pop(k)))
                        continue
            
            return result
    
    async def get_cards(self, code, instance, bot, update, msg_id):
        async with aiohttp.ClientSession() as session:
            count = 1
            next_page = f"https://5ka.ru/api/v2/special_offers/?records_per_page=15&page=1&store={code}&ordering=&price_promo__gte=&price_promo__lte=&categories=&search="
            instance.cur_for_cards.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='id{code}'")
            if len(instance.cur_for_cards.fetchall()) == 0:
                while next_page != None:
                    async with session.get(url=next_page) as response:
                        await bot.edit_message_text(chat_id=update.from_user.id,text=f"сканирую страницу {count}",
                                            message_id=msg_id)
                        json_cards = await response.json()
                        if json_cards['results'] == []:
                                raise config_pyat.NotProductsError('продуктов нет на сайте')
                        for item in json_cards['results']:  
                            instance.card_filter(item,code,instance.db_for_cards,instance.cur_for_cards)
                        next_page = json_cards['next']
                    count +=1
                instance.db_for_cards.close()
            else:
                instance.cur_for_cards.execute(f"SELECT date FROM id{code}")
                if datetime.strptime(instance.cur_for_cards.fetchone()[0], '%Y-%m-%d').date() != datetime.now().date():
                    instance.cur_for_cards.execute(f"DROP TABLE IF EXISTS id{code}")
                    while next_page != None:
                        async with session.get(url=next_page) as response:
                            await bot.edit_message_text(chat_id=update.from_user.id,text=f"сканирую страницу {count}",
                                                message_id=msg_id)
                            json_cards = await response.json()
                            if json_cards['results'] == []:
                                raise config_pyat.NotProductsError('продуктов нет на сайте')
                            for item in json_cards['results']:  
                                instance.card_filter(item,code,instance.db_for_cards,instance.cur_for_cards)
                            next_page = json_cards['next']
                        count +=1
                    instance.db_for_cards.close()
                else:
                    print('файл актуален!')
                    instance.db_for_cards.close()


class ScrapyPyatBot_HandMode(ScrapyPyatBot):

    def __init__(self, address):
        self.address = address
        self.db_for_cards = sqlite3.connect(config_pyat.file_path[0])
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
        


if __name__ == "__main__":
    try:
        bot = ScrapyPyatBot(54.539939,52.830721)
        print(bot.get_stores(bot.latitude,bot.longitude))
        code = input('Введи код')
        bot.get_cards(code,bot)
    except config_pyat.FindCityError as e:
        print('Магазинов пяторочки рядом не найдено!')
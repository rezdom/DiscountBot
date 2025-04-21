from enum import Enum

class UserRole(int, Enum):
    USER = 0
    ADMIN = 1

class MarketGroups(int, Enum):
    MAGNIT = 0
    PYATOROCHKA = 1

class ProductTypes(int, Enum):
    OTHER = 0
    DAIRY_EGGS = 1
    VEGETABLES_FRUITS = 2
    BAKERY = 3
    GROCERY_SAUCES = 4
    MEAT = 5
    FISH = 6
    SWEETS = 7
    TEA_COFFEE = 8
    DRINKS = 9
    SNACKS_NUTS = 10
    CHEMISTRY = 11
    ALCO = 12
class FindCityError(Exception):
    def __init__(self, errmsg) -> None:
        self.errmsg = errmsg

class NotProductsError(Exception):
    def __init__(self, errmsg) -> None:
        self.errmsg = errmsg

file_path = [
    r"source\Pyatorochka\cards_pyat_info.db",
]
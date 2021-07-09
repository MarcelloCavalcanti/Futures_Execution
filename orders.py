class StreetOrder:
    def __init__(self, order_info):
        self.id = order_info.get("id")
        self.symbol = order_info.get("security").get("symbol")
        self.load_time = order_info.get("orderLoadTime")
        self.size = order_info.get("size")
        self.id = order_info.get("id")
        self.destination = order_info.get("destination")
        self.parent_id = order_info.get("parentId")

        if order_info.get("priceType") == "Market":
            self.price_type = "M"
        else:
            self.price_type = "L"


class ParentOrder:
    def __init__(self, order_info):
        try:
            self.notes = order_info[0].get("notes")
        except:
            self.notes = None
        try:
            self.client_order_id = order_info[0].get("clientOrderId")
        except:
            self.client_order_id = None
        try:
            self.load_time = order_info[0].get("orderLoadTime")
        except:
            self.load_time = None


class StreetOrderExec:
    def __init__(self, exec_info):
        self.id = exec_info.get("id")
        self.size = exec_info.get("size")
        self.price = exec_info.get("price")
        self.last_market = exec_info.get("lastMarket")
        self.transaction_time = exec_info.get("transactionTime")
        self.type = exec_info.get("executionType")


class OrderError(Exception):
    pass


class ResponseError(Exception):
    pass

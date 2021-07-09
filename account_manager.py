import requests, os, re
import datetime as dt
import pandas as pd
import json

os.chdir('C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/')

from logger import Logger
from config_settings import Database
from orders import StreetOrder, ParentOrder, StreetOrderExec, OrderError, ResponseError


class FlexNowAuthenticate(Database):
    def __init__(self, session_type: str):
        '''
        session_type: str: 'uat' or 'live' entered to configure session login
        '''

        super().__init__()

        # demo account
        if re.search('uat|test|dev', session_type, re.I):
            self.configure_flexnow_uat_credentials()
            self.user_credentials = self.uat_credentials_map
            self.base_url = 'https://api.flexnow-uat.eu.flextrade.com/api/v5/'
            self._client_id = self.user_credentials['client_id']
            self._secret_token = self.user_credentials['token']
            self._user = self.user_credentials['user']
            self._password = self.user_credentials['psswd']
        # live account
        elif re.search('live|real|executable', session_type, re.I):
            self.configure_flexnow_live_credentials()
            self.user_credentials = self.live_credentials_map
            self.base_url = 'https://api.flexnow.eu.flextrade.com/api/v5/'
        else:
            raise (Exception('Incorect session type string initialized: check docstring'))

        # Setting url candidates
        # ----------------------------------------------------------------------------------------------------------------------
        self.token_url = 'auth/client-token'
        self.token_plus_refresh_url = 'auth/token'
        self.trefresh_url = 'auth/refresh'
        self.destinations_url = 'destinations'
        self.order_url = 'street-orders/new'
        self.orders_current = 'parent_orders/current'
        self.orders_info_url = 'street-orders'
        self.cancel_url = 'street-orders/cancel'
        self.summary_url = 'street-orders/summary?date='

        # Initialization of helper attributes
        # ----------------------------------------------------------------------------------------------------------------------
        self.logger = Logger.get_logger()
        self._access_token = None
        self._refresh_token = None
        self._token_time = None

        # Setting access token to attribute
        # ----------------------------------------------------------------------------------------------------------------------
        self.set_access_token()

    @property
    def secret_token(self):
        return self._secret_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def token_time(self):
        return self._token_time

    def generate_client_headers(self):
        """Generates HTTP headers with authorization for API requests."""
        return {"clientId": self._client_id,
                "clientSecret": self._secret_token,
                }

    def generate_user_headers(self):
        """Generates HTTP headers with authorization for API requests based on user and psswd credentials."""
        return {**self.generate_client_headers(), **{"username": self._user,
                                                     "password": self._password,
                                                     }}

    def generate_generic_headers(self):
        """Generates HTTP headers for API requests."""
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def generate_headers_with_auth(self, token_type: str = 'access'):
        """Generates HTTP headers with authorization for API requests."""
        if re.search('access', token_type, re.I):
            bearer_token = self._access_token
        elif re.search('refresh', token_type, re.I):
            bearer_token = self._refresh_token
        else:
            raise (Exception('Please check docstrings and change token_type value'))

        return {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + bearer_token
        }

    def set_access_token(self, url: str = None):
        """Authenticates with the API and returns an access token."""
        if isinstance(url, type(None)):
            url = self.base_url + self.token_plus_refresh_url

        data = self.generate_user_headers()
        response = requests.request(
            "POST", url, headers=self.generate_generic_headers(), json=data)

        self._token_time = dt.datetime.now()

        if response.status_code == 200:
            self.logger.info(msg='Access to FlexNow done. Token created')
        else:
            self.logger.warning(msg=f'Something went wrong when trying to create the token: "{response.json()}".')
            raise (Exception(f'Something went wrong when trying to refresh the token: "{response.json()}".'))

        self._access_token = json.loads(response.text).get("accessToken")
        self._refresh_token = json.loads(response.text).get("refreshToken")

    def reset_access_token(self):
        '''
        Cascading method to reset access token.
        '''

        data = {**self.generate_client_headers(), **{'refreshToken': self._refresh_token}, **{'username': self._user}}
        response = requests.request(
            "POST", self.base_url + self.trefresh_url, headers=self.generate_headers_with_auth(),
            json=data)

        self._token_time = dt.datetime.now()

        if response.status_code == 200:
            self.logger.info(msg='Access to FlexNow done. Token created')
        else:
            self.logger.warning(msg=f'Something went wrong when trying to create the token: "{response.json()}".')
            raise (Exception(f'Something went wrong when trying to refresh the token: "{response.json()}".'))

        self._access_token = json.loads(response.text).get("accessToken")
        self._refresh_token = json.loads(response.text).get("refreshToken")
        #return self


class FlexNowPost(FlexNowAuthenticate):
    def __init__(self, session_type: str):
        FlexNowAuthenticate.__init__(self, session_type=session_type)

    def execute_order(self, symbol: str, asset_class: str, currency: str, region: str, country: str, mic_code: str,
                      side: str, quantity: int, broker: str, strategy_note: str, time_in_force: str = 'Day',
                      tif_expiration_date: dt.datetime = None,
                      stop_price: float = None, limit_price: float = None, order_type: str = 'Market',
                      maturity_date: dt.datetime = None, sub_destination: str = 'CASH', booking_type: str = 'Cash'):
        """
        Required parameters: [symbol, asset_class, currency, region, country, mic_code, side, quantity, broker,
        time_in_force, strategy_note]

        symbol: str: orderable security either Bloomberg or Eikon ticker
        asset_class: str: 'Equity', 'Future', 'Option', etc.
        currency: str: 'USD', 'EUR', 'GBP', etc.
        region: str: The region in which symbol trades: 'NorthAmerica', 'SouthAmerica', 'Europe', 'Africa', 'AsiaOceania'
        country: str: The 2 character ISO 3166 country code
        mic_code: str: 4 character ISO 10383 MIC (Market Identifier Code) for the exchange at which symbol trades
        side: str: Side of the order: 'Buy', 'Sell', 'SellShort', 'ShortExempt', 'SellUndisclosed'
        quantity: int: Number of shares (or contracts for a futures order)
        destination: str: ID for the destination you want to process your order
        strategy_note: str: To distinguish between strategies and perform PnL attribution
        time_in_force: str = 'Day': The time in force for the order: 'Day', 'Gtc', 'Gtd', 'Close'
        tif_expiration_date: dt.datetime: Expiration date for order
        stop_price: float = 0: The price to be executed if StopLimit order is specified
        limit_price: float = 0: The price to be executed if Limit order is specified
        order_type: str: The price type for the order: 'Market', 'Limit', 'Stop', 'StopLimit'
        maturity_date: dt.datetime = None: The date of maturity (if applicable) to the security
        sub_destination: str = 'CASH': Sub-destination setting
        booking_type: str = 'Cash': The type of booking being made: 'Cash', 'Future', 'CFD'
        """

        # TODO: Check booking_type if 'CFD' is a possible argument

        if not isinstance(stop_price, type(None)) and not isinstance(limit_price, type(None)):
            assert (bool(re.search('StopLimit', order_type, re.I)) == True)
        elif not isinstance(stop_price, type(None)):
            assert (bool(re.search('Stop', order_type, re.I)) == True)
        elif not isinstance(limit_price, type(None)):
            assert (bool(re.search('Limit', order_type, re.I)) == True)
        else:
            pass

        url = self.base_url + self.order_url

        order_type: str = order_type.strip().lower().capitalize()

        _null_date_formatter = lambda x: None if not isinstance(x, dt.datetime) else x.strftime('%Y-%m-%d')

        if not re.search('^Market$|^Limit$|^Stop$', order_type):
            raise OrderError(f'{order_type} not recognized, please use "Market", "Limit" or "Stop" only.')
        else:
            data = [{"security": {"symbol": symbol, "bloomberg": {"tickerAndExchangeCode": None,
                                                                  "ticker": None, "yellowKey": asset_class},
                                  "eikon": None,
                                  "assetClass": asset_class, "currency": currency, "region": region, "country": country,
                                  "isin": None,
                                  "sedol": '23424242', "mic": mic_code,
                                  "maturityDate": _null_date_formatter(maturity_date)},
                     "side": side,
                     "locateId": None, "locateSubId": None,
                     "quantity": quantity, "bookingType": booking_type, "account": None, "algoPresetId": None,
                     "destination": broker,
                     "subDestination": sub_destination, "internalComment": strategy_note, "timeInForce":
                         {"type": time_in_force, "expireDate": _null_date_formatter(tif_expiration_date)},
                     "price": {"priceType": order_type,
                               "limitPrice": limit_price, "stopPrice": stop_price},
                     "clientId": self._client_id,
                     "clientSecret": self._secret_token
                     }]

        self.reset_access_token()
        response = requests.post(url, data=json.dumps(data), headers=self.generate_headers_with_auth())

        if response.status_code == 202:
            order_id = response.json()['pending'][0]['orderId']
            self.logger.info(
                msg=f'Order ID: {order_id} ({side} {quantity} {symbol}) '
                    f'has been transmitted to FLEX server.')
        else:
            self.logger.error(msg=f'API response throws an error: {response.json()}.')
            raise ResponseError(f'API response throws an error: {response.json()}.')

        return order_id

    def end(self, message='GENERIC END() exited the code'):
        self.logger.error(f'Exiting code due to: {message}')

    def example_order_string(self):
        return '''
        List [ OrderedMap { "security": OrderedMap { "symbol": "AAPL US Equity", "bloomberg":
        OrderedMap { "tickerAndExchangeCode": "AAPL US", "ticker": "AAPL", "yellowKey": "Equity" }, "eikon": null,
        "assetClass": "Equity", "currency": "USD", "region": "NorthAmerica", "country": "US", "isin": null,
        "sedol": "2046251", "mic": "XNAS", "maturityDate": null }, "side": "Buy", "locateId": null, "locateSubId": null,
         "quantity": 250, "bookingType": "Cash", "account": null, "algoPresetId": 1, "destination": "BAML",
         "subDestination": null, "internalComment": "Internal comment", "timeInForce":
         OrderedMap { "type": "Day", "expireDate": null }, "price": OrderedMap { "priceType": "Limit",
         "limitPrice": 100.25, "stopPrice": null } }, OrderedMap { "security": OrderedMap { "symbol": "QCZ9 Index",
         "bloomberg": OrderedMap { "tickerAndExchangeCode": null, "ticker": "QCZ9", "yellowKey": "Index" },
         "eikon": null, "assetClass": "Future", "currency": "SEK", "region": "Europe", "country": "SE", "isin":
         "SE0008048789", "sedol": null, "mic": "XSTO", "maturityDate": "2019-12-20" }, "side": "Buy", "locateId": null,
         "locateSubId": null, "quantity": 100, "bookingType": "Cash", "account": null, "algoPresetId": null,
         "destination": "BARC", "subDestination": "DMA", "internalComment": null, "timeInForce": OrderedMap
         { "type": "Day", "expireDate": null }, "price": OrderedMap { "priceType": "Limit", "limitPrice": 1734.75,
         "stopPrice": null } } ]
        '''


class FlexNowGet(FlexNowAuthenticate):
    def __init__(self, session_type: str):
        FlexNowAuthenticate.__init__(self, session_type=session_type)

    @property
    def destinations(self):
        return self.get_destinations_info()

    def get_street_orders(self, date=dt.datetime.today().strftime('%Y-%m-%d')):
        """Returns a list of StreetOrders for the specified date as a generator object."""
        url = f"{self.base_url}street-orders/summary?Date={date}&"
        response = requests.request(
            "GET", url, headers=self.generate_headers_with_auth())

        for order in json.loads(response.text):
            yield StreetOrder(order)

    def get_parent_order(self, order_id):
        """Returns a ParentOrder with the specified order ID."""
        if order_id is None:
            return ParentOrder({})

        url = f"{self.base_url}parent-orders/{order_id}/details"
        response = requests.request(
            "GET", url, headers=self.generate_headers_with_auth())

        return ParentOrder(json.loads(response.text))

    def get_street_order_execs(self, order_id):
        """Returns a list of StreetOrderExecs for the specified order ID"""
        url = f"{self.base_url}street-orders/{order_id}/executions"
        response = requests.request(
            "GET", url, headers=self.generate_headers_with_auth())

        for execution in json.loads(response.text):
            yield StreetOrderExec(execution)

    def check_order(self, order_id):
        url = self.base_url + self.orders_info_url
        headers = self.generate_headers_with_auth()
        response = requests.get(url, headers=headers)
        order_detail = next(item for item in response.json() if item["id"] == order_id)
        return order_detail

    def check_all_orders(self):
        url = self.base_url + self.orders_info_url
        headers = self.generate_headers_with_auth()
        response = requests.get(url, headers=headers)
        orders = response.json()
        orders = pd.DataFrame.from_dict(orders)
        return orders

    def get_summary(self, date=dt.datetime.today()):
        url = self.base_url + self.summary_url + date.strftime('%Y-%m-%d')
        headers = self.generate_headers_with_auth()
        response = requests.get(url, headers=headers)
        orders = response.json()
        orders = pd.DataFrame.from_dict(orders)
        return orders

    def cancel_orders(self, order_ids: list):
        url = self.base_url + self.cancel_url
        headers = self.generate_headers_with_auth()
        data = list(map(lambda x: str(x), order_ids))
        response = requests.post(url, data=data, headers=headers)
        rejected = response.json().get('Rejected')
        if rejected:
            self.logger.info(msg=str(rejected) + 'have been canceled')
        else:
            self.logger.info(msg=str(rejected) + 'have not been canceled')

    def get_destinations_info(self) -> list:
        return json.loads(
            requests.get(self.base_url + self.destinations_url, headers=self.generate_headers_with_auth()).text)


class FlexNowExecution(FlexNowPost, FlexNowGet):
    def __init__(self, session_type: str):
        FlexNowPost.__init__(self, session_type=session_type)
        FlexNowGet.__init__(self, session_type=session_type)


if __name__ == '__main__':
    
    FlexNowExecution(session_type='uat').execute_order(symbol='ABC', asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code='XNYS', side='BUY',
                                                       quantity=100,
                                                       broker='SOCGENsim', strategy_note='MC_test')
    
    FlexNowExecution(session_type='uat').execute_order(symbol='ABC', asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code='XNYS', side='SELL',
                                                       quantity=100, booking_type= 'Swap',
                                                       broker='SOCGENsim', strategy_note='MC_test')


import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote:str, base:str, amount: str):
        base = base.lower()
        quote = quote.lower()

        if quote == base:
            raise APIException('Базовая и котируемая валюта совпадают!')

        try:
            base_code = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            quote_code = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        url = f'https://min-api.cryptocompare.com/data/price?fsym={base_code}&tsyms={quote_code}'
        r = requests.get(url)
        jsonpart=json.loads(r.content)
        total_quote = jsonpart[keys[quote]]*amount

        return total_quote
import requests

def get_crypto_price(api_key, symbol):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if response.status_code == 200 and 'data' in data and symbol in data['data']:
        return data['data'][symbol]['quote']['USD']['price']
    else:
        raise ValueError(f"Erro ao obter o preço da criptomoeda: {data}")

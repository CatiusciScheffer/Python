import requests

def get_crypto_payment_price(api_key, symbol):
    """
    Obtém o preço atual de uma criptomoeda específica em USD usando a API da CoinMarketCap.

    Args:
        api_key (str): Chave da API da CoinMarketCap.
        symbol (str): Símbolo da criptomoeda (por exemplo, 'BTC' para Bitcoin).

    Returns:
        float: O preço atual da criptomoeda em USD.

    Raises:
        ValueError: Se ocorrer um erro ao obter o preço da criptomoeda ou se a resposta da API não for bem-sucedida.
    """
    
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {'symbol': symbol, 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if response.status_code == 200:
        if 'data' in data and symbol in data['data']:
            return data['data'][symbol]['quote']['USD']['price']
        else:
            raise ValueError(f"Dados não encontrados para o símbolo {symbol}. Resposta: {data}")
    else:
        raise ValueError(f"Erro ao obter o preço da criptomoeda: {data}")


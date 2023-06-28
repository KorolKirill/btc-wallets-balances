import requests

# Чтение адресов из файла
with open('addresses.txt', 'r') as file:
    addresses = [line.strip() for line in file]

# Суммарный баланс в биткоинах
total_balance_btc = 0

# API для получения текущего курса обмена Bitcoin
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
rate = response.json()['bpi']['USD']['rate_float']

# Перебор всех адресов и подсчет суммарного баланса
for address in addresses:
    # API BlockCypher для проверки баланса кошелька
    try:
        response = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{address}')
        balance = response.json()['balance'] / 1e8 # переводим из сатоши в биткоины
        total_balance_btc += balance
    except Exception as e:
        print(f'Невозможно получить баланс для адреса: {address}. Ошибка: {e}')
        continue

# Переводим суммарный баланс в доллары
total_balance_usd = total_balance_btc * rate

print(f'Суммарный баланс кошельков: {total_balance_btc} BTC')
print(f'Эквивалент в долларах: {total_balance_usd} USD')

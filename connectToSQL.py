import sqlite3
import json


with open('coin.json', 'r') as file:
    data = json.load(file)

conn = sqlite3.connect('coin.db')
cursor = conn.cursor()
cursor.execute(
        'CREATE TABLE IF NOT EXISTS coin (coin_id INTEGER PRIMARY KEY, coin_name TEXT, coin_symbol TEXT, coin_price REAL)')
for coin in data:
    if coin['name'] in ['Bitcoin', 'Ethereum', 'Binance Coin', 'Cardano', 'XRP', 'Dogecoin', 'Polkadot', 'Solana', 'USD Coin', 'Terra']:
        coin_id = coin['id']
        coin_name = coin['name']
        coin_symbol = coin['symbol']
        coin_price = coin['price']
        cursor.execute('UPDATE coin SET coin_price = ? WHERE coin_symbol = ?', (coin_price, coin_symbol))
conn.commit()
conn.close()
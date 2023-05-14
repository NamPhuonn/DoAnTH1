import socket
import sqlite3
import json
import ast
import requests


def get_coin_data():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': '83a2a200-4303-4bf8-b9e1-801b84ac7c31'}
    response = requests.get(url, headers=headers)

    # Kiểm tra dữ liệu trả về
    if response.status_code != 200:
        print('Error:', response.status_code)
    else:
        try:
            data = response.json()['data']
            conn = sqlite3.connect('coin.db')
            cursor = conn.cursor()
            for coin in data:
                if coin['name'] in ['Bitcoin', 'Ethereum', 'Binance Coin', 'Cardano', 'XRP', 'Dogecoin', 'Polkadot', 'Solana', 'USD Coin', 'Terra']:
                    coin_id = coin['id']
                    coin_name = coin['name']
                    coin_symbol = coin['symbol']
                    coin_price = coin['quote']['USD']['price']
                    cursor.execute('UPDATE coin SET coin_price = ? WHERE coin_symbol = ?', (coin_price, coin_symbol))
            conn.commit()
            conn.close()
        except KeyError as e:
            print('Error:', e)


def get_all_coins():
    # Lấy danh sách các đồng tiền và giá của chúng
    conn = sqlite3.connect('coin.db')
    cursor = conn.cursor()

    cursor.execute('SELECT coin_name, coin_price FROM coin')
    result = cursor.fetchall()

    conn.close()

    coins_dict = dict(result)
    return coins_dict


def get_coin_price(coin_symbol):
    # Lấy giá của một đồng tiền cụ thể
    conn = sqlite3.connect('coin.db')
    cursor = conn.cursor()

    cursor.execute( 'SELECT coin_price FROM coin WHERE coin_symbol = ?', (coin_symbol,))
    result = cursor.fetchone()

    conn.close()

    return result[0]


def handle_request(client_socket, request):
    # Xử lý yêu cầu từ client
    if request == 'MARKET ALL':
        response_data = get_all_coins()
    elif 'MARKET' in request:
        coin_symbol = request.split()[1]
        response_data = get_coin_price(coin_symbol)
    else:
        response_data = 'Invalid request'

    # Gửi kết quả trả về cho client
    response = {'status': 'OK', 'data': response_data}
    response_str = json.dumps(response)
    client_socket.send(response_str.encode())


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8000

    # Kết nối đến cơ sở dữ liệu và lấy thông tin giá cryptocurrency
    conn = sqlite3.connect('coin.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS coin (coin_id INTEGER PRIMARY KEY, coin_name TEXT, coin_symbol TEXT, coin_price REAL)')
    conn.commit()
    conn.close()
    get_coin_data()

    # Thiết lập server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print('Server is running on {}:{}'.format(HOST, PORT))

    while True:
        client_socket, address = server_socket.accept()
        print('Client is connected from', address)

        # Nhận yêu cầu từ client và xử lý yêu cầu
        request_str = client_socket.recv(4096).decode()
        request = ast.literal_eval(request_str)['data']
        handle_request(client_socket, request)

        client_socket.close()

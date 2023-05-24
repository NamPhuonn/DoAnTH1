import socket
import sqlite3
import json
from connectToAPI import *
import threading

def get_coin_data():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': '83a2a200-4303-4bf8-b9e1-801b84ac7c31'}
    header, content = send_get_request(url, headers=headers)

    status_code = get_status_code(header.decode())
    # Kiểm tra dữ liệu trả về
    if status_code != 200:
        print('Error:', status_code)
    else:
        try:
            data = response_to_json(content)
            conn = sqlite3.connect('coin.db')
            cursor = conn.cursor()
            for coin in data:
                if coin['name'] in ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'USD Coin', 'XRP', 'Cardano', 'Dogecoin', 'Polygon', 'Solana']:
                    coin_id = coin['id']
                    coin_name = coin['name']
                    coin_symbol = coin['symbol']
                    coin_price = coin['price']
                    # Chèn hoặc cập nhật dữ liệu
                    cursor.execute('INSERT OR REPLACE INTO coin (coin_id, coin_name, coin_symbol, coin_price) VALUES (?, ?, ?, ?)', (coin_id, coin_name, coin_symbol, coin_price))
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

    return float(result[0])


def handle_client(client_socket):
    # Xử lý yêu cầu từ một client
    while True:
        # Nhận yêu cầu từ client
        request_str = client_socket.recv(4096).decode()
        if not request_str:
            break
        request = json.loads(request_str)['data']
        print('Client: ' + request)
        # Xử lý yêu cầu
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

        # Tạo một luồng mới để xử lý yêu cầu từ client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


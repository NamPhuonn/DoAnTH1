import socket
import ast

def connect_to_server():
    # Kết nối đến server
    HOST = '127.0.0.1'
    PORT = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket

def display_menu():
    # Hiển thị menu cho người dùng và lấy yêu cầu tra cứu
    print('1. Tra cứu danh sách các đồng tiền và giá qui đổi của đồng tiền tương ứng')
    print('2. Tra cứu 1 đồng tiền và giá qui đổi của đồng tiền đó')
    choice = input('Vui lòng chọn tính năng (1 hoặc 2): ')

    if choice == '1':
        request = {'status': 'OK', 'data': 'MARKET ALL'}
    elif choice == '2':
        coin_symbol = input('Nhập mã của đồng tiền (VD: BTC): ')
        request_data = 'MARKET ' + coin_symbol.upper()
        request = {'status': 'OK', 'data': request_data}
    else:
        print('Bạn đã nhập lựa chọn không hợp lệ!')
        request = None

    return request

def send_request(client_socket, request):
    # Gửi yêu cầu đến server và nhận kết quả trả về
    request_str = str(request)
    client_socket.send(request_str.encode())
    response_str = client_socket.recv(1024).decode()
    response = ast.literal_eval(response_str)['data']

    return response

def display_result(result):
    # Hiển thị kết quả tra cứu cho người dùng
    if isinstance(result, dict):
        for coin_name, coin_price in result.items():
            print(coin_name, ':', coin_price)
    elif isinstance(result, float):
        print('Giá của đồng tiền:', result)
    else:
        print(result)

if __name__ == '__main__':
    client_socket = connect_to_server()

    while True:
        request = display_menu()

        if request:
            result = send_request(client_socket, request)
            display_result(result)

    client_socket.close()

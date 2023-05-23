import socket
import json
import ssl

def send_get_request(url, headers=None):
    # Phân tích URL để lấy thông tin về host và đường dẫn
    host, path = parse_url(url)
    
    # Tạo ngữ cảnh SSL
    context = ssl.create_default_context()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bọc socket với SSL
    client_socket = context.wrap_socket(client_socket, server_hostname=host)
    client_socket.connect((host, 443))

    # Gửi yêu cầu GET
    request = build_get_request(host, path, headers)
    client_socket.sendall(request.encode())
    
    # Nhận và trả về phản hồi từ máy chủ
    header, content = receive_response(client_socket)

    substring = b',{"id":1958,'
    content = content.split(substring)[0]
    content += b']}}'

    client_socket.close()
    return header, content

def parse_url(url):
    # Tách host và path từ URL
    url_parts = url.split('/')
    host = url_parts[2]
    path = '/' + '/'.join(url_parts[3:])
    return host, path

def build_get_request(host, path, headers):
    request = f"GET {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    
    if headers:
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
    
    request += "\r\n"
    return request

def receive_response(client_socket):
    response = b""
    while True:
        data = client_socket.recv(4096)
        response += data
        if b"\r\n0\r\n\r\n" in response:
            break

    # Chia phản hồi thành phần tiêu đề và nội dung
    header_end = response.find(b"\r\n\r\n")
    header = response[:header_end]
    content_start = header_end + 4
    content_end = response.rfind(b"\r\n0\r\n\r\n")
    content = response[content_start:content_end]
    content = content[content.index(b'{'):]

    return header, content

def get_status_code(header):
    # Tách mã trạng thái từ phản hồi HTTP
    status_line = header.split('\r\n')[0]
    status_code = int(status_line.split(' ')[1])
    return status_code

def response_to_json(data):
    data = data.decode('utf8')
    data_start = data.find('"data":[') + 8
    data_section = data[data_start:-5]

    values = []
    start_index = 0
    while True:
        id_start = data_section.find('"id":', start_index)
        if id_start == -1:
            break

        id_end = data_section.find(',', id_start)
        id_value = data_section[id_start + 5:id_end]

        name_start = data_section.find('"name":', id_end)
        name_end = data_section.find(',', name_start)
        name_value = data_section[name_start + 8:name_end]

        symbol_start = data_section.find('"symbol":', name_end)
        symbol_end = data_section.find(',', symbol_start)
        symbol_value = data_section[symbol_start + 10:symbol_end]

        price_start = data_section.find('"price":', symbol_end)
        price_end = data_section.find(',', price_start)
        price_value = data_section[price_start + 8:price_end]

        values.append({"id": id_value, "name": name_value, "symbol": symbol_value, "price": price_value})

        start_index = price_end

    return values

# Sử dụng hàm send_get_request() với headers
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {'Accepts': 'application/json',
           'X-CMC_PRO_API_KEY': '83a2a200-4303-4bf8-b9e1-801b84ac7c31'}
header, content = send_get_request(url, headers)

status_code = get_status_code(header.decode())
print(f"Status code: {status_code}")

json_data = response_to_json(content)
print(json_data)


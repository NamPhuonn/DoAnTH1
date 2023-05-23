import sqlite3
import json

# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect('coin.sql')
cursor = conn.cursor()

# Lấy dữ liệu từ bảng coin
cursor.execute("SELECT * FROM coin")
rows = cursor.fetchall()

# Chuyển đổi dữ liệu từ tuple sang danh sách đối tượng JSON
data = []
for row in rows:
    coin_id, coin_name, coin_symbol, coin_price = row
    coin = {
        'coin_id': coin_id,
        'coin_name': coin_name,
        'coin_symbol': coin_symbol,
        'coin_price': coin_price
    }
    data.append(coin)

# Chuyển đổi danh sách dữ liệu thành chuỗi JSON
json_data = json.dumps(data)

# In dữ liệu
print(json_data)

# Đóng kết nối tới cơ sở dữ liệu SQLite
conn.close()

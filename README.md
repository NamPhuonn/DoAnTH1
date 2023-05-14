# DoAnTH1
Tóm tắt cách thức làm:
Đầu tiên, bạn cần xem xét cách kết nối và gửi yêu cầu giữa client và server bằng cách sử dụng Socket. Trong Python, bạn có thể sử dụng thư viện socket để tạo ra kết nối giữa client và server.
Bên cạnh đó, bạn cần có một cơ sở dữ liệu để lưu trữ thông tin giá cryptocurrency. Bạn có thể sử dụng SQLite hoặc MySQL để tạo ra cơ sở dữ liệu và lưu trữ các thông tin này. Hoặc đơn giản là bạn có thể hard-code các thông tin này trong mã chương trình.
Khi đã có kết nối giữa client và server, bạn có thể sử dụng giao thức để gửi yêu cầu từ client đến server và trả về kết quả mong muốn. Đối với mỗi yêu cầu của client, server sẽ truy xuất cơ sở dữ liệu để lấy thông tin cryptocurrency và phản hồi lại client.
Cuối cùng, nếu bạn muốn sử dụng API để lấy thông tin cryptocurrency, bạn có thể sử dụng thư viện requests để kết nối và lấy dữ liệu từ API.
Tóm lại, để bắt đầu viết mã, bạn cần phải xác định cách kết nối và truyền thông giữa client và server sử dụng Socket, lựa chọn cơ sở dữ liệu để lưu trữ thông tin giá cryptocurrency, xác định cách gửi yêu cầu và trả về kết quả phù hợp, và trong trường hợp cần thiết, tìm hiểu cách sử dụng thư viện API để lấy thông tin ngoài.
Chi tiết hơn chút:
Chạy file thì cần chạy sever.py trước rồi mới chạy client.py và server luôn luôn đc mở để client còn gọi
*Lưu ý: Trong đoạn code có sử dụng thư viện request (Chúng ta không được sử dụng thư viện này, đây chỉ là demo kết quả)

-	Thiết kế cơ sở dữ liệu và lấy thông tin giá cryptocurrency từ API
Nó sẽ cần key API mà trong file cô có đề cập, trong code t đã dán sẵn key rồi nên nếu chưa hết hạn thì cứ sử dụng. 

-	Thiết kế cơ sở dữ liệu gồm các trường coin_id, coin_name, coin_symbol, và coin_price.
-	Dùng thư viện requests để kết nối đến API và lấy thông tin giá của các đồng tiền, và lưu vào cơ sở dữ liệu.
->Khi chạy file server.py sẽ tạo ra 1 file coin.db chứa database của 10 đồng tiền

Cơ sở dữ liệu chỉ cần chứa thông tin của 10 đồng tiền.
-	Thiết kế server
Sử dụng thư viện socket để tạo kết nối giữa client và server.
Khi nhận được yêu cầu tra cứu toàn bộ các đồng tiền, server sẽ truy vấn cơ sở dữ liệu và trả về danh sách các đồng tiền và giá của chúng cho client.
Khi nhận được yêu cầu tra cứu một đồng tiền cụ thể, server sẽ truy vấn cơ sở dữ liệu và trả về giá của đồng tiền đó cho client.
-	Thiết kế client
Khi khởi động, client sẽ yêu cầu kết nối đến server.
Sau đó, client sẽ hiển thị giao diện và cho phép người dùng chọn giữa hai tính năng tra cứu danh sách các đồng tiền và tra cứu một đồng tiền cụ thể.
Client sẽ gửi yêu cầu tương ứng đến server và hiển thị kết quả trả về trên giao diện.
Mấy cái lấy database này với connect trao đổi client-sv-api này khá ez nên giờ mình cần viết lại file server.py với client.py khi không được sử dụng thư viện request thôi. Xong cái đó rồi xử lý đa luồng nữa là xong.
Này chắc chia ra 2 đứa xử lý file. 1 đứa làm chính 1 đứa phụ
Rồi đứa phụ với đứa còn lại đi coi đa luồng.
Ai thích làm phần nào thì pick :>
Hạn làm xử lý file cho đến ngày 15 đi rồi coi đa luồng là ok

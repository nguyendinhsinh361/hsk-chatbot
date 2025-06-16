# Hướng dẫn sử dụng Environment cho HSK Chatbot API

## Giới thiệu

File `hsk-chatbot-postman-environment.json` là một Postman Environment được tạo ra để sử dụng với HSK Chatbot API Collection. Environment này chứa các biến cần thiết cho việc test API.

## Cách import Environment

1. Mở Postman
2. Nhấp vào tab "Environments" ở thanh bên trái
3. Nhấp vào nút "Import" ở phía trên
4. Chọn file `hsk-chatbot-postman-environment.json`
5. Environment "HSK Chatbot Environment" sẽ được thêm vào danh sách môi trường của bạn

## Các biến trong Environment

Environment này bao gồm các biến sau:

1. `base_url`: URL cơ sở của HSK Chatbot API (mặc định: `http://localhost:8000`)
2. `session_id`: Biến này sẽ được tự động cập nhật khi bạn gửi request đến endpoint chat

## Cách sử dụng Environment

1. Sau khi import environment, chọn "HSK Chatbot Environment" từ dropdown ở góc trên bên phải của Postman
2. Nếu server của bạn không chạy ở `http://localhost:8000`, hãy nhấp vào biểu tượng "eye" (👁️) bên cạnh dropdown environment để mở Quick Look
3. Chỉnh sửa giá trị của `base_url` cho phù hợp với địa chỉ server của bạn
4. Đóng Quick Look và tiếp tục sử dụng collection

## Thay đổi base_url

Nếu bạn cần thay đổi `base_url` vĩnh viễn:

1. Nhấp vào tab "Environments" ở thanh bên trái
2. Nhấp vào "HSK Chatbot Environment"
3. Tìm biến `base_url` và thay đổi giá trị của nó
4. Nhấp vào nút "Save" để lưu thay đổi

## Lưu ý

- Biến `session_id` sẽ được tự động cập nhật bởi script test trong collection mỗi khi bạn gửi request đến endpoint chat
- Bạn không cần phải chỉnh sửa biến `session_id` thủ công
- Đảm bảo rằng bạn đã chọn đúng environment trước khi chạy các request trong collection 
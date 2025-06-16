# Hướng dẫn sử dụng Postman Collection để test HSK Chatbot API

## Giới thiệu

File `hsk-chatbot-api-collection.json` là một Postman Collection được tạo ra để test các API endpoints có trong HSK Chatbot. Collection này bao gồm các requests cho tất cả API endpoints hiện có trong ứng dụng.

## Cài đặt

1. Tải và cài đặt [Postman](https://www.postman.com/downloads/)
2. Mở Postman
3. Nhấp vào "Import" và chọn file `hsk-chatbot-api-collection.json`
4. Collection "HSK Chatbot API" sẽ được thêm vào workspace của bạn

## Thiết lập môi trường

1. Trong Postman, tạo một môi trường mới bằng cách nhấp vào "Environments" ở thanh bên trái, sau đó nhấp vào "+" để tạo môi trường mới
2. Đặt tên cho môi trường (ví dụ: "HSK Chatbot Local")
3. Thêm biến `base_url` với giá trị `http://localhost:8000` (hoặc URL khác nếu server của bạn chạy ở địa chỉ khác)
4. Lưu môi trường
5. Chọn môi trường vừa tạo từ dropdown ở góc trên bên phải của Postman

## Các API Endpoints

Collection bao gồm các requests sau:

### 1. Root Endpoint (GET /api/)

Endpoint gốc trả về thông báo chào mừng.

### 2. Health Check (GET /api/health)

Endpoint kiểm tra trạng thái hoạt động của API.

### 3. Chat with Gemini (Graph) (POST /api/chat)

Gửi tin nhắn đến chatbot sử dụng model Gemini và phương pháp graph-based:

```json
{
    "user_input": "Xin chào, tôi muốn học tiếng Trung",
    "model_provider": "gemini",
    "use_graph": true
}
```

### 4. Chat with Gemini (Simple Chain) (POST /api/chat)

Gửi tin nhắn đến chatbot sử dụng model Gemini và phương pháp simple chain:

```json
{
    "user_input": "你好，我想学习汉语",
    "model_provider": "gemini",
    "use_graph": false
}
```

### 5. Chat with OpenAI (Graph) (POST /api/chat)

Gửi tin nhắn đến chatbot sử dụng model OpenAI và phương pháp graph-based:

```json
{
    "user_input": "HSK 1 là gì?",
    "model_provider": "openai",
    "use_graph": true
}
```

### 6. Chat with OpenAI (Simple Chain) (POST /api/chat)

Gửi tin nhắn đến chatbot sử dụng model OpenAI và phương pháp simple chain:

```json
{
    "user_input": "What is HSK?",
    "model_provider": "openai",
    "use_graph": false
}
```

### 7. Chat with Session ID (POST /api/chat)

Tiếp tục cuộc trò chuyện sử dụng session_id đã có:

```json
{
    "user_input": "Tiếp tục câu chuyện của chúng ta",
    "session_id": "{{session_id}}",
    "model_provider": "gemini",
    "use_graph": true
}
```

## Tự động lưu Session ID

Collection này có một script test tự động lưu `session_id` từ mỗi response chat thành biến môi trường `session_id`, cho phép bạn dễ dàng tiếp tục cuộc trò chuyện qua nhiều requests.

## Các yêu cầu API

1. Server HSK Chatbot cần phải đang chạy (thường là ở http://localhost:8000)
2. API keys cần được cấu hình đúng trong server (OPENAI_API_KEY và GOOGLE_API_KEY)

## Lưu ý quan trọng

- Đảm bảo rằng server đang chạy trước khi thử nghiệm API
- Đảm bảo rằng các API keys đã được cấu hình đúng trong file .env của server
- Nếu bạn gặp lỗi, hãy kiểm tra logs của server để biết thêm thông tin 
# TravelBuddy - AI Travel Planning Agent 🧳

TravelBuddy là một trợ lý du lịch thân thiện được xây dựng bằng **LangChain** và **LangGraph**, giúp bạn lên kế hoạch du lịch một cách dễ dàng.

## ✨ Tính Năng

- 🔍 **Tìm kiếm vé máy bay** giữa các thành phố Việt Nam
- 🏨 **Tìm kiếm khách sạn** với nhiều mức giá khác nhau
- 💰 **Tính toán ngân sách** du lịch
- 🤖 **AI Agent thông minh** dùng GPT-4o-mini để hiểu ý định người dùng
- 💬 **Trò chuyện tự nhiên** bằng tiếng Việt


## ⚙️ Cài Đặt

### 1. Clone repository

```bash
git clone https://github.com/vinhkhuong123/2A202600467_lab4.git
cd lab4_agent
```

### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key

Tạo file `.env` trong thư mục gốc:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Sử Dụng

### Chạy agent

```bash
python agent.py
```


## 📁 Cấu Trúc Thư Mục

```
lab4_agent/
├── agent.py                 # File chính - LangGraph agent
├── tools.py                 # Định nghĩa các tools (flights, hotels, budget)
├── system_prompt.txt        # Prompt hệ thống cho AI
├── test_api.py             # Script test API
├── test_result.md          # Kết quả test
├── requirements.txt        # Dependencies
├── .env                    # API keys (không commit)
├── .gitignore             # Git ignore rules
└── README.md              # file hướng dẫn
```



### Test Flight Search
```python
from tools import search_flights

results = search_flights("Hà Nội", "Đà Nẵng")
for flight in results:
    print(f"{flight['airline']}: {flight['departure']} - {flight['arrival']} ({flight['price']:,} VND)")
```

#
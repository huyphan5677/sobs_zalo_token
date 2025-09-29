# 🚀 Zalo OA Token Generator

Python application for automated Zalo Official Account OAuth token generation and API management.

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-sobs__zalo__token-black.svg)](https://github.com/huyphan5677/sobs_zalo_token.git)

## ✨ Features

- 🔐 **Automated OAuth Flow** - One-click token generation
- 🌐 **Built-in HTTP Server** - Handles OAuth callbacks automatically  
- 🎮 **Interactive Menu** - User-friendly command-line interface
- 📝 **API Client Wrapper** - Ready-to-use Zalo OA API methods
- ⚙️ **Configuration Management** - Centralized settings
- 🔄 **Token Management** - Automatic validation and refresh

## Cau hinh

1. **Chinh sua file `config.py`:**
   - Dien `APP_ID` va `APP_SECRET` tu Zalo Developer Console
   - Kiem tra `REDIRECT_URI` da duoc dang ky

2. **Yeu cau:**
   - Python 3.6+
   - Cac thu vien: requests

## Cach su dung

### CACH NHANH - Chi chay 1 file:

```bash
python run.py
```

File `run.py` se tu dong:
- Kiem tra cau hinh
- Kiem tra access token hien tai
- Tu dong lay token moi neu can
- Cung cap menu tuong tac de su dung API

### CACH THU CONG:

#### 1. Lay Access Token

```bash
python zalo_oauth.py
```

- Trinh duyet se mo tu dong
- Dang nhap Zalo va cap quyen cho ung dung
- Access token se duoc luu vao `zalo_access_token.txt`

#### 2. Su dung API Client

```bash
python zalo_api_client.py
```

#### 3. Menu tuong tac (trong run.py)

```
1. Show OA Information        - Xem thong tin OA
2. Test API Client           - Test cac API
3. Get New Access Token      - Lay token moi
4. Show Token Info           - Xem thong tin token
5. Send Test Message         - Gui tin nhan test
0. Exit                      - Thoat
```

#### 4. Su dung trong code:

```python
from zalo_api_client import ZaloOAClient

# Khoi tao client
client = ZaloOAClient("your_access_token")

# Lay thong tin OA
result = client.get_oa_info()
if result['success']:
    print(result['data'])

# Gui tin nhan
result = client.send_text_message("user_id", "Hello World!")
```

## Cau truc file

- `config.py` - Cau hinh ung dung
- `zalo_oauth.py` - Lay access token
- `zalo_api_client.py` - Client de goi API
- `zalo_access_token.txt` - File chua access token

## API co san

- `get_oa_info()` - Lay thong tin OA
- `get_oa_profile()` - Lay profile OA
- `send_text_message()` - Gui tin nhan text
- `get_followers()` - Lay danh sach followers

## Luu y

- Access token co thoi han 25 gio
- Can refresh token khi het han
- Port 3000 phai trong de chay OAuth server

## 🔧 Installation & Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/huyphan5677/sobs_zalo_token.git
   cd sobs_zalo_token
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Configure Zalo App:**
   - Go to [Zalo Developer Console](https://developers.zalo.me)
   - Create new app or use existing one
   - Add `http://localhost:3000` to Authorized redirect URIs
   - Copy App ID and App Secret to `config.py`

## 📚 Documentation

- [Zalo Developer Console](https://developers.zalo.me)
- [Zalo OA API Documentation](https://developers.zalo.me/docs)
- [OAuth 2.0 Flow](https://developers.zalo.me/docs/api/official-account-api/oauth)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Support

If this project helps you, please give it a ⭐ on GitHub!
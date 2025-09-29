# -*- coding: utf-8 -*-
"""
Zalo OA Configuration File
Cau hinh thong tin ung dung Zalo OA
"""

# ==========================================
# ZALO APP CONFIGURATION
# ==========================================

# Thong tin ung dung tu Zalo Developer Console
# https://developers.zalo.me
APP_ID = ""          # THAY ĐỔI APP ID MỚI Ở ĐÂY
APP_SECRET = ""  # THAY ĐỔI APP SECRET MỚI Ở ĐÂY

# Callback URL (phai duoc dang ky trong Zalo Developer Console)
REDIRECT_URI = "http://localhost:3000"

# State parameter (co the thay doi)
OAUTH_STATE = "zalo_oa_auth_2025"

# ==========================================
# API ENDPOINTS
# ==========================================

# OAuth URLs
OAUTH_AUTHORIZE_URL = "https://oauth.zaloapp.com/v4/oa/permission"
OAUTH_TOKEN_URL = "https://oauth.zaloapp.com/v4/oa/access_token"

# Zalo OA API Base URLs
OA_API_BASE_URL = "https://openapi.zalo.me/v2.0"
OA_API_V3_BASE_URL = "https://openapi.zalo.me/v3.0"

# ==========================================
# SERVER CONFIGURATION
# ==========================================

# Local server cho OAuth callback
LOCAL_SERVER_HOST = "localhost"
LOCAL_SERVER_PORT = 3000

# Timeout cho OAuth process (seconds)
OAUTH_TIMEOUT = 300  # 5 phut

# ==========================================
# FILE PATHS
# ==========================================

# File de luu access token
TOKEN_FILE = "zalo_access_token.txt"
LOG_FILE = "zalo_oauth_log.txt"

# ==========================================
# API TEST ENDPOINTS
# ==========================================

# Cac endpoint de test access token
TEST_ENDPOINTS = {
    "oa_info": "/oa/getoa",
    "oa_profile": "/oa/getprofile", 
    "oa_followers": "/oa/getfollowers"
}

# ==========================================
# HƯỚNG DẪN SỬ DỤNG
# ==========================================

"""
CÁCH SỬ DỤNG:

1. Truy cập Zalo Developer Console: https://developers.zalo.me
2. Tạo ứng dụng mới hoặc sử dụng ứng dụng có sẵn
3. Lấy App ID và App Secret từ developer console
4. Thêm http://localhost:3000 vào Authorized redirect URIs
5. Điền thông tin vào file config.py này
6. Chạy: python zalo_oauth.py

CÁC BƯỚC CHI TIẾT:
- Mở https://developers.zalo.me
- Đăng nhập bằng tài khoản Zalo
- Chọn "My Apps" > "Create App" hoặc chọn app có sẵn  
- Copy "App ID" và paste vào APP_ID
- Copy "App Secret" và paste vào APP_SECRET
- Vào "Settings" > "OAuth Settings"
- Thêm "http://localhost:3000" vào "Authorized redirect URIs"
- Lưu cấu hình
"""
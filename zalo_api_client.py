# -*- coding: utf-8 -*-
"""
Zalo OA API Client
Su dung access token de goi cac Zalo OA API
"""

import requests
import json
from config import *


class ZaloOAClient:
    """Client de goi Zalo OA APIs"""
    
    def __init__(self, access_token):
        """
        Khoi tao client voi access token
        
        Args:
            access_token (str): Access token da lay duoc
        """
        self.access_token = access_token
        self.headers = {
            'access_token': access_token,
            'Content-Type': 'application/json'
        }
    
    def get_oa_info(self):
        """
        Lay thong tin Official Account
        
        Returns:
            dict: Thong tin OA hoac error
        """
        url = f"{OA_API_BASE_URL}/oa/getoa"
        
        try:
            response = requests.get(url, headers={'access_token': self.access_token})
            return self._handle_response(response)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_oa_profile(self):
        """
        Lay profile cua OA
        
        Returns:
            dict: Profile OA hoac error
        """
        url = f"{OA_API_BASE_URL}/oa/getprofile"
        
        try:
            response = requests.get(url, headers={'access_token': self.access_token})
            return self._handle_response(response)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_text_message(self, user_id, message):
        """
        Gui tin nhan text den user
        
        Args:
            user_id (str): ID cua user nhan tin nhan
            message (str): Noi dung tin nhan
            
        Returns:
            dict: Ket qua gui tin nhan
        """
        url = f"{OA_API_BASE_URL}/oa/message"
        
        data = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": message
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            return self._handle_response(response)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_followers(self, offset=0, count=10):
        """
        Lay danh sach followers
        
        Args:
            offset (int): Vi tri bat dau
            count (int): So luong can lay
            
        Returns:
            dict: Danh sach followers hoac error
        """
        url = f"{OA_API_BASE_URL}/oa/getfollowers"
        
        params = {
            'data': json.dumps({
                'offset': offset,
                'count': count
            })
        }
        
        try:
            response = requests.get(url, headers={'access_token': self.access_token}, params=params)
            return self._handle_response(response)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_response(self, response):
        """
        Xu ly response tu API
        
        Args:
            response: Response object tu requests
            
        Returns:
            dict: Ket qua da xu ly
        """
        try:
            if response.status_code == 200:
                data = response.json()
                
                if data.get('error') == 0:
                    return {
                        'success': True,
                        'data': data.get('data', data)
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('message', 'API Error'),
                        'error_code': data.get('error')
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'status_code': response.status_code
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Response parsing error: {str(e)}"
            }


def load_token_from_file(file_path=TOKEN_FILE):
    """
    Doc access token tu file
    
    Args:
        file_path (str): Duong dan den file chua token
        
    Returns:
        str or None: Access token hoac None neu khong doc duoc
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ACCESS TOKEN:'):
                    return line.replace('ACCESS TOKEN:', '').strip()
        return None
    except Exception as e:
        print(f"Error reading token file: {e}")
        return None


def main():
    """Ham chinh de test API client"""
    print("=" * 60)
    print("ZALO OA API CLIENT TEST")
    print("=" * 60)
    
    # Doc token tu file
    access_token = load_token_from_file()
    
    if not access_token:
        print("Error: No access token found")
        print(f"Please run 'python zalo_oauth.py' first to get access token")
        return
    
    print(f"Using access token: {access_token[:50]}...")
    
    # Khoi tao client
    client = ZaloOAClient(access_token)
    
    # Test cac API
    print("\n1. Testing OA Info API...")
    result = client.get_oa_info()
    if result['success']:
        oa_data = result['data']
        print(f"   OA Name: {oa_data.get('name', 'N/A')}")
        print(f"   OA ID: {oa_data.get('oa_id', 'N/A')}")
        print(f"   Description: {oa_data.get('description', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n2. Testing OA Profile API...")
    result = client.get_oa_profile()
    if result['success']:
        print(f"   Profile data: {json.dumps(result['data'], indent=2, ensure_ascii=False)}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n3. Testing Get Followers API...")
    result = client.get_followers(count=5)
    if result['success']:
        followers = result['data'].get('followers', [])
        print(f"   Total followers: {result['data'].get('total', 0)}")
        print(f"   First 5 followers: {len(followers)} found")
        for i, follower in enumerate(followers[:3], 1):
            print(f"   {i}. User ID: {follower.get('user_id', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 60)
    print("API Test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
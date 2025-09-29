# -*- coding: utf-8 -*-
"""
Zalo OA Manager - Main Runner
File chinh de quan ly toan bo quy trinh Zalo OA
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta

# Import modules
try:
    from config import *
    from zalo_oauth import start_oauth_flow
    from zalo_api_client import ZaloOAClient, load_token_from_file
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure all required files are in the same directory")
    sys.exit(1)


class ZaloOAManager:
    """Quan ly toan bo quy trinh Zalo OA"""
    
    def __init__(self):
        self.access_token = None
        self.token_info = None
        self.client = None
    
    def check_config(self):
        """Kiem tra cau hinh"""
        print("Checking configuration...")
        
        if not APP_ID or APP_ID == "YOUR_APP_ID_HERE":
            print("Error: APP_ID not configured")
            print("Please edit config.py and set your APP_ID")
            return False
        
        if not APP_SECRET or APP_SECRET == "YOUR_APP_SECRET_HERE":
            print("Error: APP_SECRET not configured") 
            print("Please edit config.py and set your APP_SECRET")
            return False
        
        print(f"  App ID: {APP_ID}")
        print(f"  Redirect URI: {REDIRECT_URI}")
        print("Configuration OK")
        return True
    
    def check_token(self):
        """Kiem tra access token hien tai"""
        print("Checking existing access token...")
        
        if not os.path.exists(TOKEN_FILE):
            print(f"  Token file not found: {TOKEN_FILE}")
            return False
        
        # Doc token tu file
        self.access_token = load_token_from_file()
        if not self.access_token:
            print("  Could not read access token from file")
            return False
        
        # Doc thong tin chi tiet tu file
        self.token_info = self.parse_token_file()
        
        # Kiem tra thoi han
        if self.token_info and 'expires_time' in self.token_info:
            if datetime.now() > self.token_info['expires_time']:
                print("  Access token has expired")
                return False
        
        # Test token
        if self.test_token():
            print(f"  Access token is valid: {self.access_token[:50]}...")
            return True
        else:
            print("  Access token is invalid or expired")
            return False
    
    def parse_token_file(self):
        """Doc thong tin chi tiet tu token file"""
        try:
            info = {}
            with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Parse cac thong tin
                lines = content.split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower().replace(' ', '_')
                        value = value.strip()
                        
                        if key == 'generated':
                            try:
                                info['generated_time'] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                            except:
                                pass
                        elif key == 'expires_in':
                            try:
                                expires_seconds = int(value.split()[0])
                                if 'generated_time' in info:
                                    info['expires_time'] = info['generated_time'] + timedelta(seconds=expires_seconds)
                            except:
                                pass
                        elif key in ['oa_name', 'oa_id', 'app_id']:
                            info[key] = value
            
            return info
        except Exception as e:
            print(f"  Error parsing token file: {e}")
            return {}
    
    def test_token(self):
        """Test access token"""
        try:
            client = ZaloOAClient(self.access_token)
            result = client.get_oa_info()
            return result.get('success', False)
        except:
            return False
    
    def get_new_token(self):
        """Lay access token moi"""
        print("Getting new access token...")
        print("This will open your browser for OAuth authorization")
        
        try:
            start_oauth_flow()
            
            # Kiem tra lai sau khi OAuth
            time.sleep(2)
            return self.check_token()
            
        except Exception as e:
            print(f"Error during OAuth flow: {e}")
            return False
    
    def initialize_client(self):
        """Khoi tao API client"""
        if self.access_token:
            self.client = ZaloOAClient(self.access_token)
            return True
        return False
    
    def show_oa_info(self):
        """Hien thi thong tin OA"""
        if not self.client:
            return
        
        print("\nOA Information:")
        print("-" * 40)
        
        result = self.client.get_oa_info()
        if result['success']:
            data = result['data']
            print(f"Name: {data.get('name', 'N/A')}")
            print(f"ID: {data.get('oa_id', 'N/A')}")
            print(f"Description: {data.get('description', 'N/A')[:100]}...")
        else:
            print(f"Error: {result['error']}")
    
    def show_menu(self):
        """Hien thi menu lua chon"""
        print("\n" + "=" * 50)
        print("ZALO OA MANAGER")
        print("=" * 50)
        
        if self.token_info:
            print(f"Current OA: {self.token_info.get('oa_name', 'Unknown')}")
            if 'expires_time' in self.token_info:
                remaining = self.token_info['expires_time'] - datetime.now()
                hours = int(remaining.total_seconds() / 3600)
                print(f"Token expires in: {hours} hours")
        
        print("\nOptions:")
        print("1. Show OA Information")
        print("2. Test API Client")
        print("3. Get New Access Token")
        print("4. Show Token Info")
        print("5. Send Test Message (if you have user_id)")
        print("0. Exit")
        print("-" * 50)
    
    def interactive_mode(self):
        """Che do tuong tac"""
        while True:
            self.show_menu()
            choice = input("Select option (0-5): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                self.show_oa_info()
            elif choice == '2':
                self.test_api_client()
            elif choice == '3':
                if self.get_new_token():
                    self.initialize_client()
                    print("New token obtained successfully!")
                else:
                    print("Failed to get new token")
            elif choice == '4':
                self.show_token_info()
            elif choice == '5':
                self.send_test_message()
            else:
                print("Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def test_api_client(self):
        """Test API client"""
        if not self.client:
            print("No API client available")
            return
        
        print("\nTesting API Client...")
        print("-" * 40)
        
        # Test OA Info
        print("1. OA Info API:")
        result = self.client.get_oa_info()
        if result['success']:
            print("   SUCCESS")
        else:
            print(f"   ERROR: {result['error']}")
        
        # Test Get Followers (might fail due to API version)
        print("2. Get Followers API:")
        result = self.client.get_followers(count=1)
        if result['success']:
            print("   SUCCESS")
        else:
            print(f"   ERROR: {result['error']}")
    
    def show_token_info(self):
        """Hien thi thong tin token"""
        print("\nToken Information:")
        print("-" * 40)
        
        if self.token_info:
            for key, value in self.token_info.items():
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print("No token information available")
        
        if self.access_token:
            print(f"Access Token: {self.access_token[:50]}...")
    
    def send_test_message(self):
        """Gui tin nhan test"""
        if not self.client:
            print("No API client available")
            return
        
        user_id = input("Enter user ID to send test message (or press Enter to skip): ").strip()
        if not user_id:
            print("Skipped")
            return
        
        message = input("Enter message text (default: 'Hello from Zalo OA!'): ").strip()
        if not message:
            message = "Hello from Zalo OA!"
        
        print(f"Sending message to {user_id}...")
        result = self.client.send_text_message(user_id, message)
        
        if result['success']:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {result['error']}")
    
    def run(self):
        """Chay chuong trinh chinh"""
        print("=" * 60)
        print("ZALO OA MANAGER - MAIN RUNNER")
        print("=" * 60)
        
        # Kiem tra cau hinh
        if not self.check_config():
            return False
        
        # Kiem tra token hien tai
        if not self.check_token():
            print("\nNo valid access token found.")
            choice = input("Do you want to get a new access token? (y/n): ").lower().strip()
            
            if choice == 'y':
                if not self.get_new_token():
                    print("Failed to get access token. Exiting.")
                    return False
            else:
                print("Cannot proceed without access token. Exiting.")
                return False
        
        # Khoi tao client
        if not self.initialize_client():
            print("Failed to initialize API client")
            return False
        
        # Vao che do tuong tac
        self.interactive_mode()
        
        return True


def main():
    """Ham chinh"""
    try:
        manager = ZaloOAManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
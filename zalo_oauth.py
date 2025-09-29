# -*- coding: utf-8 -*-
"""
Zalo OA OAuth Client
Lay access token cho Zalo Official Account
"""

import requests
import urllib.parse
import webbrowser
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Import configuration
from config import *


class ZaloOAuthHandler(BaseHTTPRequestHandler):
    """Handler cho OAuth callback"""
    
    def do_GET(self):
        """Xu ly GET request cho OAuth callback"""
        if self.path.startswith('/?'):
            # Parse URL parameters
            from urllib.parse import parse_qs, urlparse
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            if 'code' in params:
                code = params['code'][0]
                oa_id = params.get('oa_id', ['N/A'])[0]
                state = params.get('state', ['N/A'])[0]
                
                print(f"Received authorization code: {code[:50]}...")
                print(f"OA ID: {oa_id}")
                print(f"State: {state}")
                
                # Xu ly ngay lap tuc
                result = self.exchange_code_for_token(code, oa_id)
                html_response = self.generate_html_response(code, oa_id, result)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_response.encode('utf-8'))
                
                # Luu ket qua vao server
                self.server.oauth_result = result
                
            else:
                self.send_error_response("No authorization code found")
        else:
            self.send_error_response("Invalid callback URL")
    
    def exchange_code_for_token(self, auth_code, oa_id):
        """Doi authorization code thanh access token"""
        print("Exchanging authorization code for access token...")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'secret_key': APP_SECRET
        }
        
        data = {
            'code': auth_code,
            'app_id': APP_ID,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(OAUTH_TOKEN_URL, headers=headers, data=data)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'access_token' in result:
                    print("SUCCESS! Got access token")
                    
                    # Test access token
                    test_result = self.test_access_token(result['access_token'])
                    
                    # Luu vao file
                    self.save_token_to_file(result, oa_id, test_result)
                    
                    return {
                        'success': True,
                        'access_token': result['access_token'],
                        'refresh_token': result.get('refresh_token', 'N/A'),
                        'expires_in': result.get('expires_in', 'N/A'),
                        'test_result': test_result
                    }
                else:
                    error_msg = result.get('error_description', result.get('message', 'Unknown error'))
                    print(f"API Error: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"HTTP Error: {error_msg}")
                return {'success': False, 'error': error_msg}
                
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            print(f"Exception: {error_msg}")
            return {'success': False, 'error': error_msg}
    
    def test_access_token(self, access_token):
        """Test access token voi OA API"""
        print("Testing access token...")
        
        test_url = f"{OA_API_BASE_URL}/oa/getoa"
        headers = {'access_token': access_token}
        
        try:
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('error') == 0 and 'data' in result:
                    oa_data = result['data']
                    return {
                        'success': True,
                        'oa_name': oa_data.get('name', 'N/A'),
                        'oa_id': oa_data.get('oa_id', 'N/A'),
                        'description': oa_data.get('description', 'N/A')
                    }
                else:
                    return {'success': False, 'error': result.get('message', 'API Error')}
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': f"Exception: {str(e)}"}
    
    def save_token_to_file(self, token_data, oa_id, test_result):
        """Luu access token vao file"""
        try:
            with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("ZALO OA ACCESS TOKEN\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"App ID: {APP_ID}\n")
                f.write(f"OA ID: {oa_id}\n")
                
                if test_result['success']:
                    f.write(f"OA Name: {test_result['oa_name']}\n")
                    f.write(f"Verified OA ID: {test_result['oa_id']}\n")
                
                f.write("-" * 60 + "\n")
                f.write(f"ACCESS TOKEN: {token_data['access_token']}\n")
                f.write(f"REFRESH TOKEN: {token_data.get('refresh_token', 'N/A')}\n")
                f.write(f"EXPIRES IN: {token_data.get('expires_in', 'N/A')} seconds\n")
                f.write(f"TEST STATUS: {'SUCCESS' if test_result['success'] else 'FAILED'}\n")
                
                if not test_result['success']:
                    f.write(f"TEST ERROR: {test_result['error']}\n")
                
                f.write("=" * 60 + "\n")
            
            print(f"Token saved to: {TOKEN_FILE}")
            
        except Exception as e:
            print(f"Error saving token file: {str(e)}")
    
    def generate_html_response(self, code, oa_id, result):
        """Tao HTML response cho browser"""
        if result['success']:
            status_class = "success"
            status_text = "THANH CONG"
            
            token_info = f"""
            <div class="info">
                <h3>Access Token Information</h3>
                <p><strong>Access Token:</strong> <code>{result['access_token']}</code></p>
                <p><strong>Refresh Token:</strong> {result['refresh_token']}</p>
                <p><strong>Expires In:</strong> {result['expires_in']} seconds</p>
            </div>
            """
            
            if result['test_result']['success']:
                test_info = f"""
                <div class="info success">
                    <h3>OA Information</h3>
                    <p><strong>OA Name:</strong> {result['test_result']['oa_name']}</p>
                    <p><strong>OA ID:</strong> {result['test_result']['oa_id']}</p>
                    <p><strong>Status:</strong> Token is working!</p>
                </div>
                """
            else:
                test_info = f"""
                <div class="info error">
                    <h3>Test Failed</h3>
                    <p><strong>Error:</strong> {result['test_result']['error']}</p>
                </div>
                """
        else:
            status_class = "error"
            status_text = "THAT BAI"
            token_info = f"""
            <div class="info error">
                <h3>Error</h3>
                <p>{result['error']}</p>
            </div>
            """
            test_info = ""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Zalo OA OAuth Result</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .info {{ background: #f8f9fa; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
                .info.success {{ border-left-color: #28a745; background: #d4edda; }}
                .info.error {{ border-left-color: #dc3545; background: #f8d7da; }}
                code {{ background: #e9ecef; padding: 2px 5px; border-radius: 3px; font-family: monospace; word-break: break-all; }}
                h1 {{ text-align: center; }}
                .status {{ text-align: center; font-size: 24px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Zalo OA OAuth Result</h1>
                
                <div class="status {status_class}">
                    {status_text}
                </div>
                
                <div class="info">
                    <h3>Authorization Info</h3>
                    <p><strong>Authorization Code:</strong> <code>{code[:50]}...</code></p>
                    <p><strong>OA ID:</strong> {oa_id}</p>
                </div>
                
                {token_info}
                {test_info}
                
                <div class="info">
                    <h3>File Saved</h3>
                    <p>Token information has been saved to: <code>{TOKEN_FILE}</code></p>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p>You can close this window now.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_error_response(self, error_msg):
        """Gui error response"""
        html = f"""
        <html>
            <head><meta charset="utf-8"></head>
            <body>
                <h2>Error</h2>
                <p>{error_msg}</p>
            </body>
        </html>
        """
        self.send_response(400)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override log message to reduce noise"""
        pass


def create_oauth_url():
    """Tao OAuth authorization URL"""
    params = {
        'app_id': APP_ID,
        'redirect_uri': REDIRECT_URI,
        'state': OAUTH_STATE
    }
    
    return f"{OAUTH_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def start_oauth_flow():
    """Bat dau OAuth flow"""
    print("=" * 60)
    print("ZALO OA OAUTH CLIENT")
    print("=" * 60)
    print(f"App ID: {APP_ID}")
    print(f"Redirect URI: {REDIRECT_URI}")
    print("=" * 60)
    
    # Tao OAuth URL
    oauth_url = create_oauth_url()
    print(f"OAuth URL: {oauth_url}")
    
    try:
        # Khoi dong local server
        server = HTTPServer((LOCAL_SERVER_HOST, LOCAL_SERVER_PORT), ZaloOAuthHandler)
        server.oauth_result = None
        
        print(f"\nStarting server at {REDIRECT_URI}")
        print("Please authorize the application in your browser...")
        
        # Chay server trong thread rieng
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Mo browser
        try:
            webbrowser.open(oauth_url)
            print("Browser opened automatically")
        except:
            print("Could not open browser automatically")
            print(f"Please open this URL in your browser: {oauth_url}")
        
        print("\nWaiting for OAuth callback...")
        print("Press Ctrl+C to stop")
        
        # Cho cho den khi co ket qua
        start_time = time.time()
        while server.oauth_result is None:
            if time.time() - start_time > OAUTH_TIMEOUT:
                print(f"\nTimeout after {OAUTH_TIMEOUT} seconds")
                break
            time.sleep(1)
        
        if server.oauth_result and server.oauth_result.get('success'):
            print("\n" + "=" * 60)
            print("SUCCESS! Access token received")
            print(f"Token saved to: {TOKEN_FILE}")
            print("=" * 60)
        
        server.shutdown()
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {LOCAL_SERVER_PORT} is already in use")
            print("Please close any application using this port or change LOCAL_SERVER_PORT in config.py")
        else:
            print(f"Server error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    start_oauth_flow()
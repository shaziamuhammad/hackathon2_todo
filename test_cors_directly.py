import requests
import json

def test_cors_configuration():
    '''Test the current CORS configuration'''
    print('Testing CORS configuration...')
    
    # Test server health
    try:
        resp = requests.get('http://localhost:8000/')
        print(f'Server health check: {resp.status_code}')
    except:
        print('Server is not running on http://localhost:8000')
        print('Please start your FastAPI server before running this test')
        return
    
    # Test CORS preflight
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
    }
    
    try:
        resp = requests.options('http://localhost:8000/api/v1/auth/register', headers=headers)
        print(f'CORS preflight test: {resp.status_code}')
        cors_headers = [h for h in resp.headers.keys() if 'cors' in h.lower() or 'origin' in h.lower()]
        for header in cors_headers:
            print(f'  {header}: {resp.headers[header]}')
    except Exception as e:
        print(f'CORS preflight test failed: {e}')
    
    print('\nTo test this properly, please start your FastAPI server and run: python -c "exec(open(\"debug_cors.py\").read())"')

if __name__ == '__main__':
    test_cors_configuration()

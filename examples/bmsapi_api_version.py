import bmsxmlrpc.client as xmlrpclib

ENDPOINT = 'http://127.0.0.1:8442/'
PROXY= {
        'proxy_path': '127.0.0.1:1080',
        'proxy_type': 'SOCKS5',
        'proxy_username': None,
        'proxy_password': None,
        'proxy_remotedns': True,
        'proxy_timeout': 30,
        }

def print_bms_client_info():
    api = xmlrpc.safeBMAPI(ENDPOINT, proxy=PROXY)
    result = yield from api.clientStatus()
    print(result.result if result.error == 0 else result.errormsg)

if __name__ == '__main__':
    print_bms_client_info()

# Standard library imports...
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

import re
import socket
from threading import Thread

# Third-party imports...
try:
    from xmlrpclib import Fault, dumps as xmlrpc_dumps
except ImportError:
    from xmlrpc.client import Fault, dumps as xmlrpc_dumps

RESPONSES = {}
fault = Fault(4, "exc_type:exc_value")
mfault = {"faultCode": 5, "faultString": "exc_type:exc_value"}
inboxmsg = '{"inboxMessage": [{"msgid": "msgid1", "toAddress": "BM-toAddress"}]}'

inboxmsgids_alt = '{"InboxMessages": 2}'
inboxmsgids = '{"inboxMessageIds": [{"msgid": "msgid1"}, {"msgid": "msgid2"}]}'

RESPONSES['/test_xmlrpc_ok'] = {'content': 1}
RESPONSES['/test_xmlrpc_fault'] = {'content': fault}
RESPONSES['/test_api_20'] = {'content': 'API Error 0020: Invalid method: foo'}
RESPONSES['/test_http_500'] = {'status': 500, 'content': 'I am really broken', 'rtype': 'text/plain'}

#only dict or list is valid
RESPONSES['/test_multicall_withfault'] = {'content': [[inboxmsg], [inboxmsgids], mfault]}

R404 = {'status': 404, 'content': b'No such page', 'rtype': 'text/plain'}

class MockServerRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        _res = RESPONSES.get(self.path, R404)
        self.send_response(_res.get('status', 200))
        self.send_header('Content-Type', _res.get('rtype', 'text/xml'))

        _ret = _res['content']
        if isinstance(_ret, Fault):
            results = xmlrpc_dumps(_ret, allow_none=False, encoding='utf-8')
        else:
            results = xmlrpc_dumps((_ret,), methodresponse=1, allow_none=False, encoding='utf-8')

        results = results.encode('utf-8')
        self.send_header("Content-Length", str(len(results)))
        self.end_headers()

        self.wfile.write(results)
        return


#    def do_GET(self):


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

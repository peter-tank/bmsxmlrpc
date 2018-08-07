# Third-party imports...

from unittest import TestCase, skipIf
try:
    from mock import patch, Mock, MagicMock
except ImportError as err:
    from unittest.mock import patch, Mock, MagicMock

from nose.tools import assert_dict_contains_subset, assert_list_equal, assert_true

# Local imports...
import bmsxmlrpc.client as xmlrpclib
from bmsxmlrpc.tests.mocks import get_free_port, start_mock_server

test_port = get_free_port()

def print_result(response):
    print('response =', response)
    print(response.result if response.error == 0 else response.errormsg)

class TestMockServer(object):

    @classmethod
    def setup_class(cls):
        start_mock_server(test_port)

    def test_XML_RPC_error(cls):
        client = xmlrpclib.safeBMAPI('not_exist_scheme://localhost:%d/'% (test_port))
        response = client.foo()
        print_result(response)
        assert_true(response.error == 1)  # Not prepared for method calling

    def test_connection_refused(cls):
        client = xmlrpclib.safeBMAPI('http://not_exist_ip:80/test_xmlrpc_ok')  # not exist ip:port
        response = client.foo()
        print_result(response)
        assert_true(response.error in [-3, -99])

    def test_http_500(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/test_http_500' % (test_port))
        response = client.foo()
        print_result(response)
        assert_true(response.error == -1)  # -1:ProtocolError

    def test_404_error(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/404'% (test_port))
        response = client.foo()
        print_result(response)
        assert_true(response.error == -1)  # result in ProtocolError

    def test_xmlrpc_ok(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/test_xmlrpc_ok' % (test_port))
        response = client.foo()
        print_result(response)
        assert_true(response.result == 1)

    def test_api_no_method_error(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/test_api_20' % (test_port))
        response = client.foo()
        print_result(response)
        assert_true(response.error == 20)

    def test_xmlrpc_fault(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/test_xmlrpc_fault' % (test_port))
        response = client.callfault()
        print_result(response)
        assert_true(response.error == 4)  # 4 return default fault error code

    def test_multicall_withfault(cls):
        client = xmlrpclib.safeBMAPI('http://localhost:%d/test_multicall_withfault' % (test_port))
        multicall = xmlrpclib.MultiCall(client)
        multicall.getInboxMessageById('foo')  # 0
        multicall.notvalidformulticall()  # skiped
        multicall.getAllInboxMessageIds_alt()  # 1
        multicall.getInboxMessageById()  # 2 return fault fault error code
        responses = multicall()

        for response in responses:
            print_result(response)
        assert_true(responses[0].result[0]['msgid'] == "msgid1")
        assert_true(responses[1].result['InboxMessages'] == 2)
        assert_true(responses[2].error == 5)

def failing_request(*args, **kwargs):
    raise OSError


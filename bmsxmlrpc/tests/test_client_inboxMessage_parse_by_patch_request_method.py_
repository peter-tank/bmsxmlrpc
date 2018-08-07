# Standard library imports...

from unittest import TestCase, skipIf

try:
    from mock import patch, Mock, MagicMock
except ImportError:
    from unittest.mock import patch, Mock, MagicMock

# Third-party imports...
from nose.tools import assert_is_none, assert_list_equal, assert_true

# Local imports...
import bmsxmlrpc.client as xmlrpclib
from bmsxmlrpc.constants import SKIP_REAL

class TestinboxMessage(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('xmlrpclib.xmlrpclib.ServerProxy.__transport.request')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_msg_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True

        message = '{"inboxMessage": [{"msgid": "0123456", "toAddress": "BM-ADDRESS"}]}'

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.json.return_value = message

        rpc = xmlrpclib.safeBMAPI('http://1.2.3.4:8442/')
        # Call the service, which will send a request to the server.
        response = rpc.getInboxMessageById('foo')

        # If the request is sent successfully, then I expect a response to be returned.
        assert_true(response.error == 0)
        assert_true(response.result[0]['msgid'] == '0123456')
        assert_true(response.result[0]['toAddress'] == 'BM-ADDRESS')


class TestinboxMessageMultiCall(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('xmlrpclib.xmlrpclib.ServerProxy.__transport.request')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_msg_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True

        message = [[{"inboxMessage": [{"msgid": "0123456", "toAddress": "BM-ADDRESS"}]}], [{"inboxMessage":[{ "msgid": "7890", "toAddress": "BM-ADDRESS1"}]}]]

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.json.return_value = message

        rpc = xmlrpclib.safeBMAPI('http://1.2.3.4:8442/')
        # Call the service, which will send a request to the server.
        multicall = xmlrpclib.MultiCall(rpc)
        multicall.getInboxMessageById('foo')
        multicall.getInboxMessageById('foo1')
        response = multicall()

        # If the request is sent successfully, then I expect a response to be returned.
        assert_true(response[0].error == 0)
        assert_true(response[0].result[0]['msgid'] == '0123456')
        assert_true(response[0].result[0]['toAddress'] == 'BM-ADDRESS')
        assert_true(response[1].error == 0)
        assert_true(response[1].result[0]['msgid'] == '7890')
        assert_true(response[1].result[0]['toAddress'] == 'BM-ADDRESS1')


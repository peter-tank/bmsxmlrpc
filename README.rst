=========
bmsxmlrpc
=========


.. image:: https://travis-ci.org/peter-tank/bmsxmlrpc.png?branch=master
   :target: https://travis-ci.org/peter-tank/bmsxmlrpc


Getting Started
===============

PyBitmessage version of the standard lib ``xmlrpc``

Currently only ``bmsxmlrpc.client``, which works like ``xmlrpc.client``,
but with proxy and API return value pre-checking supported.


Getting Started
===============

Cloning

::

    git clone https://github.com/peter-tank/bmsxmlrpc
    cd bmsxmlrpc
    git submodule init
    git submodule update
    
    --or--
    git clone --rescurse-submodule https://github.com/peter-tank/bmsxmlrpc

Updating

::

    cd bmsxmlrpc
    # merge bmsxmlrpc
    git fetch
    git merge --ff-only origin/master
    # update server
    git submodule update --remote --merge server


Installation
------------

::

    pip install bmsxmlrpc


Example of usage
----------------

This example show how to print the current version of the PyBitmessage XML-RPC api.


::

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

..

    proxy_type except `SOCKS4`, `SOCKS5`, `HTTP`
    proxy_timeout default `30`


References
----------

PyBitmessage GitHub `Repository
<https://github.com/Bitmessage/PyBitmessage>`__.


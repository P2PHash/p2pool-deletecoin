import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    DeleteCoin=math.Object(
        P2P_PREFIX='fcd9b7dd'.decode('hex'),
        P2P_PORT=45651,
        ADDRESS_VERSION=30,
        RPC_PORT=46650,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'DeleteCoin address' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 250*100000000 >> (height + 1)//1314000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='DEL',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'DeleteCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/DeleteCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.DeleteCoin'), 'DeleteCoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name

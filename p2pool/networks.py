from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    DeleteCoin=math.Object(
        PARENT=networks.nets['DeleteCoin'],
        SHARE_PERIOD=12, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=20, # shares
        SPREAD=30, # blocks
        IDENTIFIER='6d903b8d037dbc6d'.decode('hex'),
        PREFIX='1a51e3fc0471daef'.decode('hex'),
        P2P_PORT=22052,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=22053,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-del',
        VERSION_CHECK=lambda v: True,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name

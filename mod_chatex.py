
import logging

import game
import Keys
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import getClientLanguage
from messenger.proto.interfaces import IEntityFindCriteria
from messenger.m_constants import BATTLE_CHANNEL, PROTO_TYPE
from messenger import MessengerEntry

class MOD:
    ID = '${mod_id}'
    PACKAGE_ID = '${package_id}'
    NAME = '${name}'
    VERSION = '${version}'

_logger = logging.getLogger(MOD.NAME)

MESSAGE_DEF = {
    'en': {
        'ASSERT': 'Affirmative!',
        'NEGATE': 'Negative!'
    },
    'ja': {
        'ASSERT': '了解! (Affirmative!)',
        'NEGATE': '拒否! (Negative!)'
    }
}

class MESSAGE:
    pass

def overrideMethod(cls, method):
    def decorator(handler):
        orig = getattr(cls, method)
        newm = lambda *args, **kwargs: handler(orig, *args, **kwargs)
        if type(orig) is not property:
            setattr(cls, method, newm)
        else:
            setattr(cls, method, property(newm))
    return decorator

@overrideMethod(game, 'handleKeyEvent')
def _handleKeyEvent(orig, event):
    ret = orig(event)
    try:
        if event.isKeyDown() and not event.isRepeatedEvent():
            if event.key == Keys.KEY_F5:
                sendTeamMessage(MESSAGE.ASSERT)
            elif event.key == Keys.KEY_F6:
                sendTeamMessage(MESSAGE.NEGATE)
    except:
        LOG_CURRENT_EXCEPTION()
    return ret

def init():
    _logger.info('initialize: %s %s', MOD.PACKAGE_ID, MOD.VERSION)
    msglng = lng = getClientLanguage()
    if msglng not in MESSAGE_DEF:
        msglng = 'en'
    _logger.info('client language = %s, chat message language = %s', lng, msglng)
    for name, value in MESSAGE_DEF[msglng].items():
        setattr(MESSAGE, name, value)

# ex.
#   scripts/client/messenger/proto/bw/find_criteria.py
#       BWBattleTeamChannelFindCriteria
class BattleTeamChannelFindCriteria(IEntityFindCriteria):
    def filter(self, channel):
        result = False
        if channel.getProtoType() is PROTO_TYPE.BW_CHAT2:
            return channel.getProtoData().settings == BATTLE_CHANNEL.TEAM
        return result

def sendTeamMessage(text):
    criteria = BattleTeamChannelFindCriteria()
    ctrl = MessengerEntry.g_instance.gui.channelsCtrl.getControllerByCriteria(criteria)
    if ctrl is not None:
        ctrl.sendMessage(text)

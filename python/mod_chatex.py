
import os
import logging
import json
from functools import partial

import ResMgr
import Keys
from Event import Event
from PlayerEvents import g_playerEvents
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import getClientLanguage
from gui import g_keyEventHandlers
from messenger.proto.interfaces import IEntityFindCriteria
from messenger.m_constants import BATTLE_CHANNEL, PROTO_TYPE
from messenger import MessengerEntry

class MOD:
    ID = '${mod_id}'
    PACKAGE_ID = '${package_id}'
    NAME = '${name}'
    VERSION = '${version}'
    CONFIG_FILES = [
        '${resource_file}',
        '${config_file}'
    ]

_logger = logging.getLogger(MOD.NAME)

MESSAGE_DEF = {
    'en': {
        'ASSERT': 'Affirmative!',
        'NEGATE': 'Negative!'
    }
}

g_controller = None


class KeyHandler(object):
    def __init__(self):
        self.__keyEvents = {}

    def addKeyEvent(self, key, handler):
        if key not in self.__keyEvents:
            self.__keyEvents[key] = Event()
        self.__keyEvents[key] += handler

    def handleKeyEvent(self, event):
        if event.isKeyDown() and not event.isRepeatedEvent():
            handlers = self.__keyEvents.get(event.key, None)
            if handlers is not None:
                handlers()
                return True
        return False


class Controller(object):
    def __init__(self, config):
        self.keyHandler = KeyHandler()
        for name, value in config.items():
            key = getattr(Keys, name)
            self.keyHandler.addKeyEvent(key, partial(sendTeamMessage, value))
        g_playerEvents.onAvatarBecomePlayer += self.__onAvatarBecomePlayer
        g_playerEvents.onAvatarBecomeNonPlayer += self.__onAvatarBecomeNonPlayer

    def __onAvatarBecomePlayer(self):
        _logger.info('PlayerEvents: onAvatarBecomePlayer')
        g_keyEventHandlers.add(self.keyHandler.handleKeyEvent)

    def __onAvatarBecomeNonPlayer(self):
        _logger.info('PlayerEvents: onAvatarBecomeNonPlayer')
        g_keyEventHandlers.remove(self.keyHandler.handleKeyEvent)


def init():
    _logger.info('initialize: %s %s', MOD.PACKAGE_ID, MOD.VERSION)
    config = readConfig(MOD.CONFIG_FILES)
    lang = getClientLanguage()
    msglang = lang if lang in config else 'en'
    _logger.info('client language = %s, chat message language = %s', lang, msglang)
    global g_controller
    g_controller = Controller(config[msglang])


def readConfig(files):
    def encode_value(data):
        def encode_(x):
            if isinstance(x, unicode):
                x = x.encode('utf-8')
            return x
        return { k:encode_(v) for k, v in data.items() }
    config = MESSAGE_DEF.copy()
    _logger.info('cwd: %s', os.getcwd())
    for file in files:
        absfile = os.path.join('res', file)
        absfile = os.path.abspath(absfile) if os.path.isfile(absfile) else file
        if not ResMgr.isFile(file):
            continue
        _logger.info('loading config file: %s', absfile)
        section = ResMgr.openSection(file)
        try:
            data = json.loads(section.asString, object_hook=encode_value)
        except ValueError as e:
            _logger.error(e)
            continue
        config.update(data)
    #_logger.info('message settings:\n%s', json.dumps(config, ensure_ascii=False, indent=2))
    return config


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

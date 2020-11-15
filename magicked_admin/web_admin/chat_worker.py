import threading
import time
import logging

from events import EVENT_CHAT, EVENT_COMMAND
from PySide2.QtCore import QThread, QObject, Signal

logger = logging.getLogger(__name__)


class ChatSignals(QObject):
    signal_chat = Signal(str, str, str)
    signal_command = Signal(str, str, str)


class ChatWorker(QThread):

    def __init__(self, web_admin, event_manager, refresh_rate=1):
        QThread.__init__(self, None)

        self.signals = ChatSignals()

        self._web_admin = web_admin
        self._event_manager = event_manager

        self._exit = False
        self._refresh_rate = refresh_rate

    def run(self):
        while not self._exit:
            self._poll()
            time.sleep(self._refresh_rate)

    def close(self):
        self._exit = True

    def _poll(self):
        messages = self._web_admin.get_new_messages()

        for message in messages:
            logger.info("[CHAT] {} ({}): {}".format(
                message['username'], message['user_flags'], message['message'])
            )

            if message['message'][0] == '!':
                self._event_manager.emit_event(
                    EVENT_COMMAND, self.__class__,
                    username=message['username'],
                    args=message['message'][1:].split(),
                    user_flags=message['user_flags']
                )
            else:
                self.signals.signal_chat.emit(message['username'], message['message'], message['user_flags'])
                self._event_manager.emit_event(
                    EVENT_CHAT, self.__class__,
                    username=message['username'],
                    message=message['message'],
                    user_flags=message['user_flags']
                )

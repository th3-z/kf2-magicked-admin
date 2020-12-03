import logging
import time
from collections import namedtuple

from PySide2.QtCore import QThread, Slot

logger = logging.getLogger(__name__)

MessageData = namedtuple(
    'message', [
        'username', 'message', 'user_flags', 'date'
    ]
)


class ChatWorker(QThread):

    def __init__(self, server, refresh_rate=1):
        QThread.__init__(self, None)

        self.signals = server.signals
        self._web_admin = server.web_admin

        self._exit = False
        self._refresh_rate = refresh_rate

        self.signals.post_chat.connect(self.receive_post_chat)
        self.log = []

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
            self.signals.chat.emit(message['username'], message['message'], message['user_flags'])
            self.log.append(
                MessageData(message['username'], message['message'], message['user_flags'], int(time.time()))
            )

            if message['message'][0] == '!':
                self.signals.command.emit(message['username'], message['message'][1:].split(), message['user_flags'])

    @Slot(str, str, int)
    def receive_post_chat(self, username, message, user_flags):
        self._web_admin.submit_message(message)

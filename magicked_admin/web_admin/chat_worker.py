import threading
import time

from events import EVENT_CHAT, EVENT_COMMAND


class ChatWorker(threading.Thread):
    def __init__(self, web_admin, event_manager, refresh_rate=1):
        threading.Thread.__init__(self)

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
            if message['message'][0] == '!':
                self._event_manager.emit_event(
                    EVENT_COMMAND, self.__class__,
                    username=message['username'],
                    args=message['message'][1:].split(),
                    user_flags=message['user_flags']
                )
            else:
                self._event_manager.emit_event(
                    EVENT_CHAT, self.__class__,
                    username=message['username'],
                    message=message['message'],
                    user_flags=message['user_flags']
                )

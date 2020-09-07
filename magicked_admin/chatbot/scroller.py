import threading
import time
from itertools import count

from utils.text import chat_lines, chat_width, str_width, center_str
from events import EVENT_SUBMIT_MESSAGE


class Scroller(threading.Thread):
    def __init__(self, event_manager, body, head=None, loop=False, speed=8.5, time=15):
        threading.Thread.__init__(self)
        self.event_manager = event_manager

        """
        Each iteration scrolls the text one line and submits a message, the
        speed is measured in lines per second
        """
        self.speed = speed
        self.loop = loop
        self.time = time
        self._timer = 0

        if head:
            self.head_lines = [line.strip() for line in head.strip().split("\n")]
        else:
            self.head_lines = []
        self.body_lines = [line.strip() for line in body.strip().split("\n")]

    def validate_width(self):
        for line in self.body_lines + self.head_lines:
            if str_width(line) > chat_width:
                return False
        return True

    def run(self):
        for i in count(0):
            line_start = i % len(self.body_lines)
            line_end = (i + chat_lines - len(self.head_lines)) % len(self.body_lines)

            message = ""
            if line_start > line_end:
                message += "\n".join(self.body_lines[line_start:])
                if self.loop:
                    message += "\n".join(self.body_lines[:line_end])
            else:
                message += "\n".join(self.body_lines[line_start:line_end])

            head = "\n" + "\n".join(self.head_lines) + "\n"

            self.event_manager(
                EVENT_SUBMIT_MESSAGE, self.__class__, message=head + message
            )

            if line_end < line_start and not self.loop:
                break

            # FIXME: Assumes the above takes place instantly (it doesnt)
            time.sleep(1 / self.speed)
            self._timer += 1 / self.speed
            if self._timer > self.time:
                break

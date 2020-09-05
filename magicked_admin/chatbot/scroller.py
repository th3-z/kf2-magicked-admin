from utils.text import chat_lines, chat_width, str_width
import threading
from itertools import count


class Scroller(threading.Thread):
    def __init__(self, event_manager, body, head=None, loop=False, speed=8.5):
        threading.Thread.__init__(self)
        self.event_manager = event_manager

        """
        Each iteration scrolls the text one line and submits a message, the
        speed is measured in lines per second
        """
        self.speed = speed
        self.loop = loop

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
            line_end = (i + self.scroll_height - 2) % len(self.body_lines)

            message = ""
            if line_start > line_end:
                message += "\n".join(self.body_lines[:line_end])
                message += "\n".join(self.body_lines[line_start:])
            else:
                message += "\n".join(self.body_lines[line_start:line_end])

            print(message)
            print()
            print()

            title = "\n"+center_str("kills leaderboard")

            self.server.web_admin.submit_message(
                self.format_response(title+"\nRank | Kills  | Username\n" + message, args)
            )

            if line_end < line_start and not self.loop:
                break

            time.sleep(1 / self.speed)

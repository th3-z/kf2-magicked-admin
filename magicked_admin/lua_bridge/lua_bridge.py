import lupa
from lupa import LuaRuntime

from web_admin.chat import ChatListener
from utils.lua import load_script
from utils import find_data_file


class LuaBridge(ChatListener):
    def __init__(self, server, chatbot):
        # Init interpreter, create functions/namespaces in Lua's global state
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(load_script("lua_bridge/init.lua"))

        # Params: namespace, func
        self.new_bind = self.lua.eval("bind_py_func")

        # Params: namespace
        self.new_namespace = self.lua.eval("new_namespace")
        self.lua.eval("log(\"Initialisation complete\")")

        self.server = server
        self.chatbot = chatbot
        self.create_binds()

    def create_binds(self):
        commands = self.chatbot.commands

        self.new_namespace("chat")
        self.new_bind(
            "chat", "say", self.chatbot.chat.submit_message
        )

        self.new_namespace("hooks")
        # ...

        self.new_namespace("server")
        self.new_bind(
            "server", "write_players", self.server.write_all_players
        )
        self.new_bind(
            "server", "write_game", self.server.write_game_map
        )
        self.new_bind(
            "server", "get_player", self.server.get_player_by_sid
        )
        self.new_bind(
            "server", "get_players", lambda: self.server.players
        )

        self.new_namespace("motd")

    def execute_script(self, filename):
        self.lua.execute(load_script(filename))

    def execute(self, string):
        self.lua.execute(string)

    def receive_message(self, username, message, user_flags):
        # TODO: Call lua event handler
        pass



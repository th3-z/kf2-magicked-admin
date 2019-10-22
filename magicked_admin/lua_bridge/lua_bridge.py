import lupa
from lupa import LuaRuntime

from web_admin.chat import ChatListener
from utils.lua import load_script


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
        self.new_namespace("chat")
        self.new_bind("chat", self.say)

    def execute_script(self, filename):
        self.lua.execute(load_script(filename))

    def execute(self, string):
        self.lua.execute(string)

    def say(self, message):
        self.chatbot.chat.submit_message(message)

    def receive_message(self, username, message, user_flags):
        # TODO: Call lua event handler
        pass



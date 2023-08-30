from interpreter import *
from error import *


# Simple whitespace module that will force the interpreter to ignore any whitespace
class WhitespaceModule(Module):
    IDENTIFIER = "Whitespace"
    INCOMPATIBLE_IDENTIFIERS = []

    def __init__(self, whitespace=[" ", "\n", "\t", "\r"]):
        self.whitespace = whitespace

    def handle_command(self, interpreter: Interpreter):
        command = interpreter.context.command()

        if command in self.whitespace:
            return Result()

        return None

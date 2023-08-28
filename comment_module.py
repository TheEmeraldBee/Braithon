
from interpreter import *

class CommentModule(Module):
    IDENTIFIER = "Comment"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command() == '#':
            while interpreter.context.command() != '\n':
                if not interpreter.context.advance():
                    break
            return Result()

        return None

    def handle_skip(self, interpreter: Interpreter) -> Result:
        self.handle_command(interpreter)

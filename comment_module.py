from interpreter import *


class CommentModule(Module):
    IDENTIFIER = "Comment"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter):
        if interpreter.context.command() == "#":
            while interpreter.context.command() != "\n":
                if not interpreter.context.advance():
                    break
            return Result()

        return None

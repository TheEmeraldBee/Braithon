from interpreter import *
from copy import deepcopy


class ScopeModule(Module):
    IDENTIFIER = "Scope"
    INCOMPATIBLE_IDENTIFIERS = []

    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("{", "}")

    def handle_command(self, interpreter: Interpreter):
        if interpreter.context.command() == "{":
            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected '}' but got EOF"))

            modules = deepcopy(interpreter.modules)
            context = interpreter.context.current()

            result = interpreter.handle_until("}")

            if result:
                if not result.is_ok():
                    return result

            # Reset context
            interpreter.context.cursor = context.cursor
            interpreter.context.program = context.program
            interpreter.modules = modules

            return Result()
        if interpreter.context.command() == "s":
            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected '}' but got EOF"))

            if interpreter.context.command() != "{":
                return Result().with_error(
                    Error(
                        -1,
                        f"Expected '{'{'}' but found '{interpreter.context.command()}'",
                    )
                )

            if not interpreter.context.advance():
                return Result().with_error(
                    Error(
                        -1,
                        "Expected '}' but found EOF",
                    )
                )

            modules = deepcopy(interpreter.modules)
            context = interpreter.context.current()

            result = interpreter.handle_until("}")

            if result:
                if not result.is_ok():
                    return result

            # Reset context
            interpreter.context.cursor = context.cursor
            interpreter.context.program[context.cursor] = context.program[
                context.cursor
            ]
            interpreter.modules = modules

            return Result()

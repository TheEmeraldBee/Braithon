from interpreter import *


class ConditionalModule(Module):
    IDENTIFIER = "Conditional"
    INCOMPATIBLE_IDENTIFIERS = []

    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("{", "}")

    def handle_command(self, interpreter: Interpreter):
        if not interpreter.context.command() == "(":
            return None

        # ( Was found, so it could be a conditional
        # Get the conditional
        condition_1 = interpreter.context.get_num_after()

        if condition_1 == None:
            return Result().with_error(Error(-1, "If statement expected number"))

        if not interpreter.context.advance():
            return Result().with_error(Error(-1, "Expected Conditions, but found EOF"))

        sign = interpreter.context.command()

        # Get the other condition
        condition_2 = interpreter.context.get_num_after()

        if condition_2 == None:
            return Result().with_error(Error(-1, "If statement expected number"))

        if not interpreter.context.advance():
            return Result().with_error(Error(-1, "Expected ')', but found EOF"))

        if interpreter.context.command() != ")":
            return Result().with_error(
                Error(-1, f"Expected ')' but got {interpreter.context.command()}")
            )

        if not interpreter.context.advance():
            return Result().with_error(Error(-1, "Expected '{', but found EOF"))

        if interpreter.context.command() != "{":
            return Result().with_error(
                Error(-1, f"Expected '{'{'}' but got {interpreter.context.command()}")
            )

        if not interpreter.context.advance():
            return Result().with_error(Error(-1, "Expected '}', but found EOF"))

        # Apply the check
        should_run = False
        match sign:
            case "<":
                should_run = (
                    interpreter.context.program[condition_1]
                    < interpreter.context.program[condition_2]
                )
            case ">":
                should_run = (
                    interpreter.context.program[condition_1]
                    > interpreter.context.program[condition_2]
                )
            case "=":
                should_run = (
                    interpreter.context.program[condition_1]
                    == interpreter.context.program[condition_2]
                )
            case "!":
                should_run = (
                    interpreter.context.program[condition_1]
                    != interpreter.context.program[condition_2]
                )
            case _:
                return Result().with_error(
                    Error(-1, f"Expected '<', '>', '!', or '=', but got '{sign}'")
                )

        inner_block_result = interpreter.get_code_until("}")

        if not inner_block_result.is_ok():
            return inner_block_result

        inner_block = inner_block_result.unwrap()

        else_block = None

        interpreter.context.advance()
        if interpreter.context.command() == "{":
            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected '}', but found EOF"))

            else_block_result = interpreter.get_code_until("}")
            if not else_block_result.is_ok():
                return else_block_result

            else_block = else_block_result.unwrap()

        past_program = interpreter.context.current()

        interpreter.context.set_program(inner_block)

        if should_run:
            result = interpreter.handle_program()
            if not result.is_ok():
                return result

        interpreter.context.set_program(else_block)

        if not should_run:
            result = interpreter.handle_program()
            if not result.is_ok():
                return result

        interpreter.context.program_string = past_program.program_string
        interpreter.context.program_string_cursor = past_program.program_string_cursor

        return Result()

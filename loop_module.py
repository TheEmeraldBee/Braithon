from interpreter import *

class LoopModule(Module):
    IDENTIFIER = "Loop"
    INCOMPATIBLE_IDENTIFIERS = []

    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("[", "]")

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command() == '[':
            if not interpreter.context.advance():
                return Result().with_error(Error(4, "Expected ']' but found EOF"))

            past_program: Context = interpreter.context.current()

            result = interpreter.get_code_until(']')

            if not result.is_ok():
                return result

            loop = result.unwrap()

            past_program.program_string_cursor = interpreter.context.program_string_cursor

            interpreter.context.set_program(loop)

            while interpreter.context.selected_value() != 0:
                result = interpreter.handle_program()
                if not result.is_ok():
                    return result

                interpreter.context.program_string_cursor = -1

            interpreter.context.program_string = past_program.program_string
            interpreter.context.program_string_cursor = past_program.program_string_cursor

            return Result()

        if interpreter.context.command_keyword("continue"):
            interpreter.context.program_string_cursor = -1
            return Result()

        if interpreter.context.command_keyword("break("):

            number = interpreter.context.get_num_after()

            if number == None:
                return Result().with_error(Error(-1, "Expected number and then ')'"))

            if interpreter.context.command() != ')':
                return Result().with_error(Error(-1, f"Expected ) but found '{interpreter.context.command()}'"))

            print(interpreter.context.command())
            
            return Result().with_break(number)
        
        if interpreter.context.command_keyword("break"):
            interpreter.context.program_string_cursor = len(interpreter.context.program_string)
            return Result()

        if interpreter.context.command_keyword("exit"):
            return Result().with_exit()

    def handle_skip(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command() == "[":
            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected ] but found EOF"))

            result = interpreter.skip_until("]")

            if result:
                return result

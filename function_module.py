
from interpreter import *

class FunctionModule(Module):
    IDENTIFIER = "Function"
    INCOMPATIBLE_IDENTIFIERS = []

    def __init__(self):
        self.functions = {}

    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("{", "}")

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("function"):
            func_name_result = interpreter.context.get_pair_after()
            if not func_name_result.is_ok():
                return func_name_result
            func_name = func_name_result.unwrap()

            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected '{' but found EOF"))

            if interpreter.context.command() != '{':
                return Result().with_error(Error(-1, "Expected '\{' but found" + f" '{interpreter.context.command()}'"))

            if not interpreter.context.advance():
                return Result().with_error(Error(-1, "Expected '}' but found EOF"))

            func_body_result = interpreter.get_code_until("}")

            if not func_body_result.is_ok():
                return func_body_result

            func_body = func_body_result.unwrap()

            self.functions[func_name] = func_body

            return Result()

        elif interpreter.context.command() == 'r':
            func_name_result = interpreter.context.get_pair_after()
            if not func_name_result.is_ok():
                return func_name_result
            func_name = func_name_result.unwrap()

            if not func_name in self.functions:
                return Result().with_error(Error(-1, f"Function with name '{func_name}' does not exist"))

            # Run the function.
            cur_program = interpreter.context.current()
            interpreter.context.set_program(self.functions[func_name])

            result = interpreter.handle_program()
            if not result.is_ok():
                return result

            interpreter.context.program_string = cur_program.program_string
            interpreter.context.program_string_cursor = cur_program.program_string_cursor

            return Result()
                

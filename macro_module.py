from interpreter import *

class MacroModule(Module):
    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("|", "|")
    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("inline"):
            python_code_result = interpreter.context.get_pair_after("|")

            if not python_code_result.is_ok():
                return python_code_result

            python_code = python_code_result.unwrap()

            eval(python_code)

            return Result()

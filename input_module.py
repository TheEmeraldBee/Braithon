from interpreter import *

class InputModule(Module):
    IDENTIFIER = "Input"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("input"):
            type_anotation_result = interpreter.context.get_pair_after()

            if not type_anotation_result.is_ok():
                return type_anotation_result

            type_anotation = type_anotation_result.unwrap()

            in_value = input()
            match type_anotation:
                case 'str':
                    interpreter.context.set_selected(in_value)
                case 'int':
                    try:
                        interpreter.context.set_selected(int(in_value))
                    except:
                        return Result().with_error(Error(-1, f"Expected a number input but got '{in_value}'"))
                case 'code':
                    # Clone the current context
                    context = interpreter.context.current()

                    # Run the given code.
                    interpreter.context.set_program(in_value)
                    result = interpreter.handle_program()

                    if not result.is_ok():
                        return result

                    # Reset the context
                    interpreter.context.program_string = context.program_string
                    interpreter.context.program_string_cursor = context.program_string_cursor
                    
                case _:
                    return Result().with_error(Error(-1, f"Expected 'str', 'int', or 'eval', but got {type_anotation}"))

            return Result()


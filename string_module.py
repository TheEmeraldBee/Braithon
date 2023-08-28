from interpreter import *

class StringModule(Module):
    IDENTIFIER = "String"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter) -> Result:

        match interpreter.context.command():
            case 's':
                result = interpreter.context.get_pair_after()
                if result.is_ok():
                    value = result.unwrap()
                    interpreter.context.set_selected(value)
                else:
                    return result
            case 'p':
                result = interpreter.context.get_pair_after()
                if result.is_ok():
                    value = result.unwrap()
                    print(value)
                else:
                    return result
            case _:
                return None
        
        return Result()


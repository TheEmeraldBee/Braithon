from interpreter import *


class StringModule(Module):
    IDENTIFIER = "String"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter):
        match interpreter.context.command():
            case "s":
                result = interpreter.context.get_pair_after()
                if result.is_ok():
                    value = result.unwrap()
                    interpreter.context.set_selected(value)
                else:
                    return result
            case "p":
                result = interpreter.context.get_pair_after()
                if result.is_ok():
                    value = result.unwrap()
                    print(value, end="")
                else:
                    return result
            case "l":
                result = interpreter.context.get_pair_after()
                if result.is_ok():
                    value = result.unwrap()
                    print(value)
                else:
                    return result
            case "/":
                # Newline!
                print()
            case _:
                return None

        return Result()

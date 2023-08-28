from interpreter import *
from time import sleep

class TimingModule(Module):
    IDENTIFIER = "Timing"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("wait"):
            if type(interpreter.context.selected_value()) is not int:
                return Result().with_error(Error(-1, "Wait requires an int"))

            ident_result = interpreter.context.get_pair_after()
            if not ident_result.is_ok():
                return ident_result

            ident = ident_result.unwrap()

            match ident:
                case 'ms':
                    sleep(interpreter.context.selected_value() / 1000)
                case 's':
                    sleep(interpreter.context.selected_value())
                case _:
                    return Result().with_error(Error(-1, f"Wait expected 'ms', 's' but got {ident}"))
            return Result()

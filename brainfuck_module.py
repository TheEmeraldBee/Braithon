from interpreter import *

class BrainfuckModule(Module):
    IDENTIFIER = "Brainfuck"
    INCOMPATIBLE_IDENTIFIERS = ["BrainfuckExtended"]
    
    def handle_command(self, interpreter: Interpreter) -> Result:
        match interpreter.context.command():
            case '>':
                if not interpreter.context.move_cursor(1):
                    return Result().with_error(Error(2, f"Cursor was moved past program maximum ({len(context.program) - 1})"))
            case '<':
                if not interpreter.context.move_cursor(-1):
                    return Result().with_error(Error(2, "Cursor was moved behing program minimum (0)"))
            case '+':
                if not type(interpreter.context.selected_value()) is int:
                    return Result().with_error(Error(3, "Attempted to adjust value in program, but program value was not int"))
                interpreter.context.set_selected(interpreter.context.selected_value() + 1)
            case '-':
                if not type(interpreter.context.selected_value()) is int:
                    return Result().with_error(Error(2, "Attempted to adjust value in program, but program value was not int"))
                interpreter.context.set_selected(interpreter.context.selected_value() - 1)
            case ',':
                if not interpreter.context.enabled:
                    return Result()

                try:
                    interpreter.context.set_selected(int(input()))
                except:
                    return Result().with_error(Error(5, "Attempted to recieve input but the input couldn't be turned into and integer"))
            case '.':
                if not interpreter.context.enabled:
                    return Result()
                
                print(chr(interpreter.context.selected_value()))

            case _:
                # The Command Was Not Handled
                return None

        # The Command Had To Have Been Handled, 
        # and no error was returned, 
        # so return an Ok Result
        return Result()

from interpreter import *

class BrainfuckExtendedModule(Module):
    IDENTIFIER = "BrainfuckExtended"
    INCOMPATIBLE_IDENTIFIERS = ["Brainfuck"]

    def handle_command(self, interpreter: Interpreter) -> Result:

        match interpreter.context.command():
            case '>':
                number = interpreter.context.get_num_after()
                if number is not None:
                    interpreter.context.move_cursor(number)
                else:
                    interpreter.context.move_cursor(1)
            case '<':
                number = interpreter.context.get_num_after()
                if number is not None:
                    interpreter.context.move_cursor(-number)
                else:
                    interpreter.context.move_cursor(-1)
            case '$':
                number = interpreter.context.get_num_after()
                if number is None:
                    return Result().with_error(Error(-1, "Command '$' expected a number but did not find one."))

                interpreter.context.set_cursor(number)
            case '%':
                number = interpreter.context.get_num_after()
                if number is not None:
                    interpreter.context.set_selected(number)
                else:
                    interpreter.context.set_selected(0)
            case ',':
                try:
                    number = int(input())
                    interpreter.context.set_selected(number)
                except:
                    return Result().with_error(Error(-1, "Command ',' expected a number but did not find one."))
            case '^':
                print(interpreter.context.selected_value())
            case '.':
                if type(interpreter.context.selected_value()) is int and interpreter.context.selected_value() >= 0:
                    print(chr(interpreter.context.selected_value()))
                else:
                    return Result().with_error(Error(-1, "Command '.' expected a positive number value to be selected"))
            case '+':
                if not type(interpreter.context.selected_value()) is int:
                    return Result().with_error(Error(3, "Attempted to adjust value in program, but program value was not int"))

                number = interpreter.context.get_num_after()
                if number is not None:
                    interpreter.context.set_selected(interpreter.context.selected_value() + number)
                else:
                    interpreter.context.set_selected(interpreter.context.selected_value() + 1)
            case '-':
                if not type(interpreter.context.selected_value()) is int:
                    return Result().with_error(Error(3, "Attempted to adjust value in program, but program value was not int"))

                number = interpreter.context.get_num_after()
                if number:
                    interpreter.context.set_selected(interpreter.context.selected_value() - number)
                else:
                    interpreter.context.set_selected(interpreter.context.selected_value() - 1)

            case _:
                return None

        return Result()



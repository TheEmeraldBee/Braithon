from interpreter import *

class MacroModule(Module):
    IDENTIFIER = "macro"
    INCOMPATIBLE_IDENTIFIERS = []
    
    def setup(self, interpreter: Interpreter):
        interpreter.register_nest("|", "|")

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("inline"):
            python_code_result = interpreter.context.get_pair_after("|")

            if not python_code_result.is_ok():
                return python_code_result

            try:
                python_code = python_code_result.unwrap()

                exec(python_code)
            
            except (SyntaxError, NameError) as e:
                return Result().with_error(Error(-1, e))

            return Result()

        if interpreter.context.command_keyword("macro"):
            macro_result = interpreter.context.get_pair_after("|")

            if not macro_result.is_ok():
                return macro_result

            macro = macro_result.unwrap()
            tracking_macro = macro

            moves = 0

            # Time to parse the macro result
            while "[@]" in tracking_macro:
                macro = macro.replace("[@]", str(interpreter.context.selected_value()), 1)
                tracking_macro = tracking_macro.replace("[@]", "", 1)
                # Move the cursor
                interpreter.context.move_cursor(1)
                moves += 1

            while "[!]" in tracking_macro:
                macro = macro.replace("[!]", f"{interpreter.context.cursor}")
                tracking_macro = tracking_macro.replace("[!]", "", 1)
                # Move the cursor
                interpreter.context.move_cursor(1)
                moves += 1

            interpreter.context.move_cursor(-moves)

            # Now execute the macro
            context = interpreter.context.current()
            interpreter.context.set_program(macro)
            result = interpreter.handle_program()

            if not result.is_ok():
                return result

            # Reset the context's program
            interpreter.context.set_program(context.program_string)
            interpreter.context.program_string_cursor = context.program_string_cursor

            return Result()

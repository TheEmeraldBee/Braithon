from error import *
import copy

NUMBERS = "0123456789"


class Context:
    def __init__(self):
        self.program = [0] * 4096
        self.cursor = 0
        self.program_string = ""
        self.program_string_cursor = -1

    def set_program(self, program):
        if program == None:
            program = ""
        self.program_string = program
        self.program_string_cursor = -1

    def advance(self, value=1) -> bool:
        if (
            self.program_string_cursor + value >= len(self.program_string)
            or self.program_string_cursor + value < 0
        ):
            return False

        self.program_string_cursor += value
        return True

    def command(self):
        return self.program_string[self.program_string_cursor]

    # Tries to get the number following directly after the current selection
    def get_num_after(self):
        if not self.advance():
            return None

        result = ""
        while self.command() in NUMBERS:
            result += self.command()

            if not self.advance():
                break

        advanced = False
        if self.advance():
            advanced = True
            self.advance(-2)

        if result == "":
            if not advanced:
                self.advance(-1)
            return None

        return int(result)

    # Tries to get the items inside a pair of characters after the current selection
    def get_pair_after(self, pair='"', end_pair=None) -> Result:
        if end_pair == None:
            end_pair = pair

        if not self.advance():
            return Result().with_error(
                Error(-1, f"Expected char '{pair}' but found EOF")
            )

        if not self.command() == pair:
            err_command = self.command()
            self.advance(-1)
            return Result().with_error(
                Error(-1, f"Expected char '{pair}' but found '{err_command}'")
            )

        if not self.advance(1):
            self.advance(-1)
            return Result().with_error(
                Error(-1, f"Expected char '{end_pair} but found EOF'")
            )

        result = ""

        while self.command() != end_pair:
            result += self.command()

            if not self.advance(1):
                return Result().with_error(
                    Error(-1, f"Expected char '{end_pair}' but found EOF")
                )

        # This pair is finished
        return Result().with_value(result)

    def command_keyword(self, keyword) -> bool:
        start_loc = self.program_string_cursor

        # Checks for a keyword
        for character in keyword:
            if self.command() != character:
                self.program_string_cursor = start_loc
                return False
            self.advance(1)

        self.advance(-1)
        return True

    def current(self):
        return copy.deepcopy(self)

    def with_program(self, program, cursor):
        self.program = program
        self.cursor = cursor
        return self

    ############### PROGRAM FUNCTIONALITY ###############

    def move_cursor(self, distance: int) -> bool:
        if (
            self.cursor + distance >= len(self.program) - 1
            or self.cursor + distance < 0
        ):
            return False

        self.cursor += distance
        return True

    def set_cursor(self, location: int) -> bool:
        if location < 0 or location >= len(self.program) - 1:
            return False
        self.cursor = location
        return True

    def selected_value(self):
        return self.program[self.cursor]

    def set_selected(self, value):
        self.program[self.cursor] = value


class Interpreter:
    def __init__(self):
        self.modules = []
        self.disabled_modules = []
        self.context = Context()
        self.nests = []

    def disable_module(self, ident):
        for module in self.modules:
            if module.IDENTIFIER == ident:
                self.modules.remove(module)
                self.disabled_modules.append(module)
                return Result()

        return Result().with_error(
            Error(-1, f"Module {ident} either doesn't exist or is already disabled!")
        )

    def enable_module(self, ident):
        for module in self.disabled_modules:
            if module.IDENTIFIER == ident:
                self.modules.append(module)
                self.disabled_modules.remove(module)
                return Result()

        return Result().with_error(
            Error(-1, f"Module {ident} either doesn't exist or is already enabled!")
        )

    def register_nest(self, start_command: str, end_command: str):
        self.nests.append((start_command, end_command))

    def with_module(self, module):
        for mounted_module in self.modules:
            if (
                module.IDENTIFIER in mounted_module.INCOMPATIBLE_IDENTIFIERS
                or mounted_module.IDENTIFIER in module.INCOMPATIBLE_IDENTIFIERS
            ):
                raise Exception(
                    f"Module {module.IDENTIFIER} is incompatible with {mounted_module.IDENTIFIER}"
                )
            if module.IDENTIFIER == mounted_module.IDENTIFIER:
                raise Exception(
                    f"Module {module.IDENTIFIER} already exists in interpreter"
                )
        module.setup(self)
        self.modules.append(module)
        return self

    def with_modules(self, modules):
        for module in modules:
            self = self.with_module(module)
        return self

    def handle_string(self, commands: str) -> Result:
        self.context.set_program(commands)
        return self.handle_program()

    def handle_program(self) -> Result:
        while self.context.advance():
            result = self.handle_command()
            if not result.is_ok():
                return result

        return Result()

    def handle_command(self) -> Result:
        result = None
        cur_context = copy.deepcopy(self.context)
        for module in self.modules:
            temp_result = module.handle_command(self)
            if temp_result:
                if not temp_result.is_ok():
                    result = temp_result
                else:
                    return Result()

        if result:
            # Error, restore project context
            self.context = cur_context
            return result

        return Result().with_error(
            Error(1, f"Command '{self.context.command()}' is not recognized")
        )

    def handle_until(self, command):
        while self.context.command() != command:
            result = self.handle_command()

            if not result.is_ok():
                return result

            if not self.context.advance():
                return Result().with_error(
                    Error(-1, f"Expected '{command}' but found EOF")
                )

    def get_code_until(self, command) -> Result:
        start_loc = self.context.program_string_cursor

        result = self.skip_until(command)

        if result:
            return result

        end_loc = self.context.program_string_cursor

        return Result().with_value(
            self.context.program_string[start_loc:end_loc].strip()
        )

    def skip_until(self, command):
        while self.context.command() != command:
            for nest in self.nests:
                if nest[0] == self.context.command():
                    if not self.context.advance():
                        return Result().with_error(
                            Error(1, f"Expected '{nest[1]}' but found EOF")
                        )

                    result = self.skip_until(nest[1])

                    if result:
                        return result

            if not self.context.advance():
                return Result().with_error(
                    Error(1, f"Expected '{command}' but found EOF")
                )


class Module:
    IDENTIFIER = None
    INCOMPATIBLE_IDENTIFIERS = []

    def setup(self, interpreter: Interpreter):
        pass

    def handle_command(self, interpreter: Interpreter):
        raise NotImplementedError()

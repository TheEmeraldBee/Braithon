from interpreter import *


class AliasModule(Module):
    IDENTIFIER = "Alias"
    INCOMPATIBLE_IDENTIFIERS = []

    def __init__(self):
        self.aliases = {}

    def handle_command(self, interpreter: Interpreter):
        if interpreter.context.command_keyword("alias"):
            alias_name_result = interpreter.context.get_pair_after()
            if not alias_name_result.is_ok():
                return alias_name_result

            alias_name = alias_name_result.unwrap()

            # Now find the range
            alias_range_result = interpreter.context.get_pair_after("(", ")")

            if not alias_range_result.is_ok():
                return alias_range_result

            alias_range_str: str = str(alias_range_result.unwrap())

            # Split the range
            alias_range_split = alias_range_str.split("..")

            if len(alias_range_split) > 2:
                return Result().with_error(Error(-1, "Expected range with 1-2 numbers"))

            try:
                range_min = (
                    None if len(alias_range_split) == 1 else int(alias_range_split[0])
                )

                range_max = (
                    int(alias_range_split[0])
                    if len(alias_range_split) == 1
                    else int(alias_range_split[1])
                )

                if range_min != None:
                    if range_min < 0 or range_min >= interpreter.context.PROGRAM_SIZE:
                        return Result().with_error(
                            Error(-1, "Wanted range is not within program bounds")
                        )
                    if range_max < 0 or range_max >= interpreter.context.PROGRAM_SIZE:
                        return Result().with_error(
                            Error(-1, "Wanted range is not within program bounds")
                        )
                    if range_max < range_min:
                        return Result().with_error(
                            Error(-1, "Wanted max should be larger than min")
                        )
                    alias_range = list(range(range_min, range_max))
                else:
                    if range_max < 0 or range_max >= interpreter.context.PROGRAM_SIZE:
                        return Result().with_error(
                            Error(-1, "Wanted index is not within program bounds")
                        )

                    alias_range = range_max

            except:
                return Result().with_error(Error(-1, "Expected range with 1-2 numbers"))

            # Add the aliases
            self.aliases[alias_name] = alias_range

            return Result()

        for alias_key in self.aliases.keys():
            if interpreter.context.command_keyword(alias_key):
                if type(self.aliases[alias_key]) is int:
                    interpreter.context.set_cursor(self.aliases[alias_key])
                    interpreter.context.advance()
                    return Result()

                if not interpreter.context.advance():
                    return Result().with_error(Error(-1, "Expected '.' but found EOF"))

                if interpreter.context.command() != ".":
                    return Result().with_error(
                        Error(
                            -1,
                            f"Expected '.' but found '{interpreter.context.command()}'",
                        )
                    )

                # Get the number
                index = interpreter.context.get_num_after()

                if index == None:
                    return Result().with_error(
                        Error(-1, "Expected Number but did not find one")
                    )

                alias_values = self.aliases[alias_key]

                if index >= len(alias_values):
                    return Result().with_error(
                        Error(-1, "Alias accessor is out of range")
                    )

                interpreter.context.set_cursor(alias_values[index])

                return Result()

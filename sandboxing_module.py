from interpreter import *

class SandboxingModule(Module):
    IDENTIFIER = "Sandboxing"
    INCOMPATIBLE_IDENTIFIERS = []

    def handle_command(self, interpreter: Interpreter) -> Result:
        if interpreter.context.command_keyword("mod_disable"):
            identifier_result = interpreter.context.get_pair_after()

            if not identifier_result.is_ok():
                return identifier_result

            identifier = identifier_result.unwrap()

            return interpreter.disable_module(identifier)
            
        if interpreter.context.command_keyword("mod_enable"):
            identifier_result = interpreter.context.get_pair_after()

            if not identifier_result.is_ok():
                return identifier_result

            identifier = identifier_result.unwrap()

            return interpreter.enable_module(identifier)

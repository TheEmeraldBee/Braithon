from interpreter import *
from error import *
from brainfuck_module import BrainfuckModule
from whitespace_module import WhitespaceModule
from brainfuck_extended_module import BrainfuckExtendedModule
from string_module import StringModule

from prelude import FULL

class Console:
    def __init__(self, modules=FULL):
        self.interpreter: Interpreter = Interpreter().with_modules(modules)

    def run(self):
        print("Type 'QUIT' to exit")
        while True:
            command = input(">>> ")
            if command == "QUIT":
                break
            result = self.interpreter.handle_string(command)
            if not result.is_ok():
                print(result)

if __name__ == "__main__":
    Console().run()

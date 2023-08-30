import sys
from prelude import *

if len(sys.argv) < 2:
    print("Please specify a file!")
else:
    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        text = file.read()

        interpreter = Interpreter().with_modules(FULL)
        result = interpreter.handle_string(text)
        if not result.is_ok():
            print(result)

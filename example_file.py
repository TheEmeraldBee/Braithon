from prelude import *

with open("example_file.bf", 'r') as file:
    text = file.read()

    interpreter = Interpreter().with_modules(FULL)

    # Now interpret the text
    result = interpreter.handle_string(text)
    if not result.is_ok():
        print(result)


# Curious How Brainf\*ck works?
[Link](https://en.wikipedia.org/wiki/Brainfuck) To Wikepedia

# To those of you that want to know everything
Brainfuck works in a very simple way. This, does not. With the extended module enabled, you have all of the same methods that brainfuck has, + more :)

For example, you can use numbers to speed up the development process!

Ex.
```
+50
[-.]
```
This would print all of the UTF-8 Characters from 50 to 0!

As well, the following also works with numbers!
```
>
<
+
-
```

New methods include the `$` which will set the program index that is selected to the number following it.

As well as the `%` which will set the value to the number following it.

## Strings
With the `FULL` module set included, you will gain access to some string things!

Ex:
```
s"Hello World"
^
```
will set the program index to the value "Hello World", then print it.

If you want to do the same without modifying your program values, use the `p` instead of `s`, and it will bypass the set and just print out the following text!

# Things without documentation that you can figure out yourself :)
# Functions
```
function"function_name_here"{
	+50
	[.-]
	p"WOW!"
}

r"function_name_here"
```

# Scope
```
{
	+150
}
# This will print 0, because the scope was used, 
# so nothing 
# done within it was saved.
^
```

# Conditionals
```
$0 %30
$1 %50

# Numbers are program locations, not values
(1<0){
	p"This shouldn't happen"
}{
	# Else!
	p"This should happen!"
}
```

# Inputs
```
$0 input"int"
$1 input"string"

# This will run this as code!
input"code"

$0^
$1^
```

# Timing
```
$0%500
wait"ms"

%5
wait"s"
```

# Writing Modules

Custom Module Example
```python
from prelude import *

class FooModule(Module):
	def handle_command(self, interpreter: Interpreter) -> Result:
	
	if interpreter.context.command_keyword("newline"):
		print("\n")
		return Result()

```

Results should only be returned if errors exist, or if you handled the command.

Error Example: ```
```python
Result().with_error(Error(-1, "Something Broke"))
```

Ok Example:
```python
Result()
```

### For more examples, check the actual existing modules!
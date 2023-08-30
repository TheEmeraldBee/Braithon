
# Curious How Brainf\*ck works?
[Link](https://en.wikipedia.org/wiki/Brainfuck) To Wikepedia

# To those of you that want to know everything
Brainf\*ck works in a very simple way. This, does not. With the extended module enabled, 
you have all of the same methods that brainf\*ck has, + more :)

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

```
s{
	+150
	>
	+150
}

# This is selective scope, so only the index selected at the start is reverted!
^ > ^
# Output: 0150
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
$1 input"str"

# This will run this as code!
input"eval"

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

# Inline Python (Macro Module) (NOT SANDBOXED)
```
# You can run inline python!
inline|interpreter.context.set_selected(-1)|
^
```

# "Macros"
No, these are not true macros, but they are powerful!

Examples:

## Print Hello, {Selected}
```
function"Hello"{macro|p"Hello, [@]"|}
s"Emerald"
r"Hello"
```

## Print the current program cursor
```
function"Selected"{macro|p"[!]"|}
r"Selected"
>>
r"Selected"
```

## Combine the next 2 program values into 1 string!
```
function"Combine"{
	macro|s"[@][@]"|
	# Clear the other input
	> %0

	# Go Back
	<
}

s"Hello, "
>
s"World"
$0 r"Combine"
^
```

## But how?!?!
```
# Inside macros, there are 2 different ways to get information
# the [@] type will be replaced by the value of current program cursor.
# the [!] type will be replaced by the current program cursor.
# Once one is used, the program cursor will automatically be moved 1 to the right.
```

# Sandboxing
Sandboxing is super important if you are going to allow access to the codebase or run code.

You can enable and disable modules using `mod_enable"ModIdentifier"`, 
and `mod_disable"ModIdentifier"` respectively!

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

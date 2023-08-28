from error import *
from interpreter import *

# Import all default modules
from brainfuck_module import BrainfuckModule
from brainfuck_extended_module import BrainfuckExtendedModule

from loop_module import LoopModule
from conditional_module import ConditionalModule
from function_module import FunctionModule

from whitespace_module import WhitespaceModule
from string_module import StringModule
from comment_module import CommentModule
from timing_module import TimingModule
from input_module import InputModule
from scope_module import ScopeModule

from macro_module import MacroModule

# Create default module sets

# The minimal amount required to replecate brainfuck. (missing some features)
MINIMAL_SET = [
    BrainfuckModule(),
    LoopModule(),
    WhitespaceModule()
]

# Improves on the features of brainfuck without adding new commands (Other than 1)
EXTENDED_SET = [
    BrainfuckExtendedModule(),
    LoopModule(),
    CommentModule(),
    WhitespaceModule()
]

# All of the default feature sets
FULL = [
    BrainfuckExtendedModule(),
    LoopModule(),
    FunctionModule(),
    ConditionalModule(),
    ScopeModule(),
    StringModule(),
    TimingModule(),
    InputModule(),
    CommentModule(),
    WhitespaceModule()
]

FULL_PLUS = FULL + [
    MacroModule()
]

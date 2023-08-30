from error import *
from interpreter import *

# Import all default modules
from simple_base_module import SimpleBaseModule
from base_module import BaseModule

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

from sandboxing_module import SandboxingModule

from alias_module import AliasModule

# Create default module sets

# The minimal amount required to replecate brainf*ck. (missing some features)
MINIMAL_SET = [SimpleBaseModule(), LoopModule(), WhitespaceModule()]

# Improves on the features of brainf*ck without adding new commands (Other than 1)
EXTENDED_SET = [
    BaseModule(),
    LoopModule(),
    CommentModule(),
    WhitespaceModule(),
]

# All of the default feature sets
FULL = [
    BaseModule(),
    LoopModule(),
    FunctionModule(),
    ConditionalModule(),
    MacroModule(),
    AliasModule(),
    SandboxingModule(),
    ScopeModule(),
    StringModule(),
    TimingModule(),
    InputModule(),
    CommentModule(),
    WhitespaceModule(),
]

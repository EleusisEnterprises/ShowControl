# stubs/td/td.pyi

from typing import Any, List

# Global variables provided by TouchDesigner
project: Any   # The project object; has attributes like .folder
root: Any      # The network root component (/)
me: Any        # The operator running the current script

# Operator access helpers
def op(path: str) -> Any: ...
def ops(pattern: str) -> List[Any]: ...

# Base OP class stub
class OP:
    name: str
    path: str
    children: List[Any]
    parent: Any
    par: Any
    def cook(self) -> None: ...

# CHOP (Channel Operator)
class CHOP(OP):
    def chans(self) -> List[Any]: ...
    def numpyArray(self) -> Any: ...

# SOP (Surface Operator)
class SOP(OP):
    pass

# TOP (Texture Operator)
class TOP(OP):
    width: int
    height: int
    def copyNumpyArray(self, arr: Any) -> None: ...

# DAT (Data Operator)
class DAT(OP):
    text: str
    def run(self) -> None: ...
    def appendRow(self, row: List[Any]) -> None: ...

# COMP (Component)
class COMP(OP):
    def create(self, opType: str, name: str) -> Any: ...
    def destroy(self) -> None: ...

# MAT (Material Operator)
class MAT(OP):
    pass

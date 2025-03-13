from dataclasses import dataclass
from typing import Any

from . import PrintGraph, GraphMethods


@dataclass
class Test:
    name: str
    children: list["Test"]

    def __hash__(self):
        return hash(self.name) % 100

    def __str__(self):
        return f"Test<{self.name}>"


d = Test("d", [])
d.children.append(d)

c = Test("c", [])
b = Test("b", [c])
a = Test("a", [])
root = Test("root", [a, b, d])

print(
    PrintGraph(
        root,
        GraphMethods(
            children=lambda x: x.children,
        ),
    ).print()
)


@dataclass
class AstNode:
    children: list["AstNode"]

    def get_children(self):
        return self.children


@dataclass
class BinaryOp(AstNode):
    op: str

    def __init__(self, op: str, left: AstNode, right: AstNode):
        super().__init__([left, right])
        self.op = op

    def __str__(self):
        return f"<* {self.op} *>"


@dataclass
class ApplyFn(AstNode):
    fn: str

    def __init__(self, fn: str, args: list[AstNode]):
        super().__init__(args)
        self.fn = fn

    def __str__(self):
        return f"<{self.fn}(*; {len(self.children)})>"


@dataclass
class Ident(AstNode):
    name: str

    def __init__(self, name: str):
        super().__init__([])
        self.name = name

    def __str__(self):
        return f"<i:{self.name}>"


@dataclass
class Value(AstNode):
    value: Any

    def __init__(self, value: Any):
        super().__init__([])
        self.value = value

    def __str__(self):
        return f"<v:{self.value}>"


print()

methods = GraphMethods(children=AstNode.get_children)
print(PrintGraph(BinaryOp("+", Value(10), Ident("x")), methods=methods).print())
print(
    PrintGraph(
        BinaryOp("+", BinaryOp("/", Value(10), Ident("y")), Ident("x")), methods=methods
    ).print()
)


print(
    PrintGraph(
        BinaryOp(
            "+",
            ApplyFn(
                "foo",
                [
                    Value(10),
                    Ident("y"),
                    Ident("z"),
                    ApplyFn(
                        "bar",
                        [
                            Value(1),
                            Value(2),
                            Value(3),
                        ],
                    ),
                ],
            ),
            Ident("x"),
        ),
        methods=methods,
    ).print()
)

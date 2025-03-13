"""Library for priting an arbitrary object graph in a tree-like view"""

from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class GraphMethods(Generic[T]):
    """Methods that need to be implemented for the objects in the graph"""

    children: Callable[[T], list[T]]
    name: Callable[[T], str] = str
    id: Callable[[T], int] = id


@dataclass
class PrintGraph(Generic[T]):
    """Produce a string version of any object graph.

    For example, suppose we modeled a Tree as:

    @dataclass
    class TreeNode:
        children: list["TreeNode"]

    And we had some TreeNode instance `t`, we could produce a visualization of
    the tree by doing:
      PrintGraph(t, GraphMethods(children=lambda t: t.children)).run()

    What's notable here is that by passing in the appropriate callbacks as a
    GraphMethods, PrintGraph can view any arbitrary type as a graph.
    """

    root: T
    methods: GraphMethods[T]
    indent_width: int = 4

    _visited: set[int] = field(default_factory=set)

    def _print(
        self,
        obj: T,
        n_parents: int = 0,
        level: int = 0,
    ) -> str:
        id_ = self.methods.id(obj)
        name = self.methods.name(obj)
        if id_ in self._visited:
            return f"--> {name} @ {self.methods.id(obj)}"
        res = ""
        res += f"{name} @ {hex(id_)}"
        res += "\n"
        self._visited.add(id_)

        children = self.methods.children(obj)
        prefix = " " * self.indent_width
        for _ in range(n_parents):
            prefix += "│"
            prefix += " " * (self.indent_width - 1)
        prefix += " " * ((level + 1) * self.indent_width - len(prefix))
        for i, child in enumerate(children):
            res += prefix
            is_last_child = i == (len(children) - 1)
            if is_last_child:
                res += "└──" + " " * (self.indent_width - 3)
            else:
                res += "├──" + " " * (self.indent_width - 3)
            res += self._print(
                child,
                n_parents + (1 if not is_last_child else 0),
                level + 1,
            )
        return res

    def print(self) -> str:
        """Print out the graph rooted at `self.root` as a string"""
        return self._print(self.root)

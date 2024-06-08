from abc import ABC, abstractmethod
from Iterator import *

class Strategy(ABC):
    @abstractmethod
    def execute(self, is_leaf):
        pass

    @abstractmethod
    def execute_container(self):
        pass

    @abstractmethod
    def execute_leaf(self):
        pass

class Strategy_tree(Strategy):
    def __init__(self, level, is_first, is_last, parent_is_last, icon, node):
        self.level = level
        self.is_first = is_first
        self.is_last = is_last
        self.parent_is_last = parent_is_last
        self.icon = icon
        self.node = node
    
    def execute(self, is_leaf):
        if is_leaf:
            self.execute_leaf()
        else:
            self.execute_container()

    def execute_container(self):
        indent = ""
        for i in range(self.level - 1):
            if self.parent_is_last[i]:
                indent += "   "
            else:
                indent += "│  "
        connector = "└─" if self.is_last else "├─"
        print(f"{indent}{connector}{self.icon.getIconContainer()}{self.node.name}")
        self.parent_is_last.append(self.is_last)
        iter = Iterator_node(self.node)
        while iter.hasMore():
            child, first, last = iter.getNext()
            child.draw(self.level + 1, first, last, self.parent_is_last, self.icon)
        self.parent_is_last.pop()

    def execute_leaf(self):
        indent = ""
        for i in range(self.level - 1):
            if self.parent_is_last[i]:
                indent += "   "
            else:
                indent += "│  "
        connector = "└─" if self.is_last else "├─"
        if self.node.value is not None:
            print(f"{indent}{connector}{self.icon.getIconLeaf()}{self.node.name}: {self.node.value}")
        else:
            print(f"{indent}{connector}{self.icon.getIconLeaf()}{self.node.name}")


class Strategy_rectangle(Strategy):
    def __init__(self, level, is_first, is_last, parent_is_last, icon, node):
        self.level = level
        self.is_first = is_first
        self.is_last = is_last
        self.parent_is_last = parent_is_last
        self.icon = icon
        self.node = node
    
    def execute(self, is_leaf):
        if is_leaf:
            self.execute_leaf()
        else:
            self.execute_container()

    def execute_container(self):
        indent = ""
        for i in range(self.level - 1):
            indent += "│   "
        connector = "┌─" if self.level == 1 and self.is_first else '├─'
        subfix = '┐' if self.level == 1 and self.is_first else '┤'
        prefix = indent + connector + self.icon.getIconContainer()
        print(f"{prefix}{self.node.name} " + '─' * (45 - len(prefix) - len(self.node.name)) + subfix)
        self.parent_is_last.append(self.is_last)
        iter = Iterator_node(self.node)
        while iter.hasMore():
            child, first, last = iter.getNext()
            child.draw(self.level + 1, first, last, self.parent_is_last, self.icon)
        self.parent_is_last.pop()

    def execute_leaf(self):
        indent = ""
        flag = True
        for i in range(self.level - 1):
            if not self.parent_is_last[i]:
                flag = False
            indent += "│   "
        if flag and self.is_last:
            indent = '└───'
            for i in range(self.level - 2):
                indent += '───'
        connector = "┴─" if flag and self.is_last else "├─"
        subfix = '┘' if flag and self.is_last else '┤'
        if self.node.value is not None:
            prefix = indent + connector + self.icon.getIconLeaf()
            print(f"{prefix}{self.node.name}: {self.node.value} " + '─' * (
                    43 - len(prefix) - len(self.node.name) - len(self.node.value)) + subfix)
        else:
            prefix = indent + connector + self.icon.getIconLeaf()
            print(f"{prefix}{self.node.name} " + '─' * (45 - len(prefix) - len(self.node.name)) + subfix)

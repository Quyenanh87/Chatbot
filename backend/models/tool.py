from typing import Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        """Initialize a tool with name, description and function"""
        self.name = name
        self.description = description
        self.func = func

    def execute(self, input_data: str) -> str:
        """Execute the tool's function with given input"""
        return self.func(input_data) 
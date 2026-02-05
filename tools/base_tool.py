from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        Execute the tool with the given arguments.
        """
        pass

    def to_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the tool.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                }
            }
        }

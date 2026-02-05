from abc import ABC, abstractmethod
from typing import Any
from llm.client import LLMClient

class BaseAgent(ABC):
    def __init__(self, llm: LLMClient, name: str = "Base Agent"):
        self.llm = llm
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        pass

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def stream(self, prompt: str):
        pass
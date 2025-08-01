from abc import ABC, abstractmethod

class BaseScoreStrategy(ABC):
    @abstractmethod
    def calculate(self, base_score: int) -> int:
        ...

from abc import ABC, abstractmethod
from mission2.grade import Grade


class BaseGradeStrategy(ABC):
    @abstractmethod
    def get_grade(self, score: int) -> Grade:
        ...
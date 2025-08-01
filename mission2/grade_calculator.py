from mission2.base_grade_strategy import BaseGradeStrategy
from mission2.default_grade_strategy import DefaultGradeStrategy
from mission2.grade import Grade


def get_grade_strategy() -> BaseGradeStrategy:
    return DefaultGradeStrategy()

class GradeCalculator:
    def __init__(self, strategy: BaseGradeStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BaseGradeStrategy):
        self._strategy = strategy

    def calculate(self, score: int) -> Grade:
        return self._strategy.get_grade(score)
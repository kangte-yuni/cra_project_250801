from mission2.grade import Grade
from mission2.base_grade_strategy import BaseGradeStrategy


class DefaultGradeStrategy(BaseGradeStrategy):
    def get_grade(self, score: int) -> Grade:
        if score >= 50:
            return Grade.GOLD
        elif score >= 30:
            return Grade.SILVER
        else:
            return Grade.NORMAL
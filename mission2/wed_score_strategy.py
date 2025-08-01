from mission2.base_score_strategy import BaseScoreStrategy


class WeekendScoreStrategy(BaseScoreStrategy):
    def calculate(self, base_score: int) -> int:
        return base_score * 2
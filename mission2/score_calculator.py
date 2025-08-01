from mission2.base_score_strategy import BaseScoreStrategy
from mission2.day import Weekday
from mission2.default_score_strategy import DefaultScoreStrategy
from mission2.wed_score_strategy import WeekendScoreStrategy
from mission2.weekend_score_strategy import WedScoreStrategy


def get_strategy_from_day(day: str) -> BaseScoreStrategy:
    if day == Weekday.WEDNESDAY.value:
        return WedScoreStrategy()
    elif day == Weekday.SATURDAY.value or day == Weekday.SUNDAY.value:
        return WeekendScoreStrategy()
    else:
        return DefaultScoreStrategy()

class ScoreCalculator:
    def __init__(self, strategy: BaseScoreStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: BaseScoreStrategy):
        self._strategy = strategy

    def calculate(self, base_score: int) -> int:
        return self._strategy.calculate(base_score)
from mission2.base_bonus_strategy import BaseBonusStrategy
from mission2.base_score_strategy import BaseScoreStrategy
from mission2.day import Weekday
from mission2.default_bonus_strategy import DefaultBonusStrategy
from mission2.default_score_strategy import DefaultScoreStrategy
from mission2.player import Player
from mission2.wed_score_strategy import WeekendScoreStrategy
from mission2.weekend_score_strategy import WedScoreStrategy


def get_score_strategy_from_day(day: str) -> BaseScoreStrategy:
    if day == Weekday.WEDNESDAY.value:
        return WedScoreStrategy()
    elif day == Weekday.SATURDAY.value or day == Weekday.SUNDAY.value:
        return WeekendScoreStrategy()
    else:
        return DefaultScoreStrategy()

def get_bonus_strategy() -> BaseBonusStrategy:
    return DefaultBonusStrategy()

class ScoreCalculator:
    def __init__(self, strategy: BaseScoreStrategy, bonus_strategy: BaseBonusStrategy):
        self._strategy = strategy
        self._bonus_strategy = bonus_strategy

    def set_strategy(self, strategy: BaseScoreStrategy):
        self._strategy = strategy

    def set_bonus_strategy(self, bonus_strategy: BaseBonusStrategy):
        self._bonus_strategy = bonus_strategy

    def calculate(self, base_score: int) -> int:
        return self._strategy.calculate(base_score)

    def calculate_bonus(self, player: Player):
        return self._bonus_strategy.calculate(player)
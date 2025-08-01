from mission2.base_bonus_strategy import BaseBonusStrategy
from mission2.day import Weekday
from mission2.player import Player


class DefaultBonusStrategy(BaseBonusStrategy):
    def calculate(self, player: Player) -> int:
        bonus = 0
        if player.get_attendance_counts_per_day(Weekday.WEDNESDAY.value) >= 10:
            bonus += 10
        if player.get_attendance_counts_per_day(Weekday.SATURDAY.value) + \
                player.get_attendance_counts_per_day(Weekday.SUNDAY.value) >= 10:
            bonus += 10
        return bonus

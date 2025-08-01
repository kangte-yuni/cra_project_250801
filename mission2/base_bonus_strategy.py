from abc import ABC, abstractmethod

from mission2.player import Player


class BaseBonusStrategy(ABC):
    @abstractmethod
    def calculate(self, player: Player) -> int:
        ...

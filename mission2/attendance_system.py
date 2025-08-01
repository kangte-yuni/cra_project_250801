from mission2.day import Weekday
from mission2.default_bonus_strategy import DefaultBonusStrategy
from mission2.default_grade_strategy import DefaultGradeStrategy
from mission2.default_score_strategy import DefaultScoreStrategy
from mission2.grade import Grade
from mission2.grade_calculator import GradeCalculator, get_grade_strategy
from mission2.player import Player
from mission2.score_calculator import ScoreCalculator, get_score_strategy_from_day, get_bonus_strategy


class AttendanceSystem:
    def __init__(self):
        self._player_info_dict = dict()
        self._score_calculator = ScoreCalculator(strategy= DefaultScoreStrategy(), bonus_strategy= DefaultBonusStrategy())
        self._grade_calculator = GradeCalculator(strategy= DefaultGradeStrategy())

    def get_player_info_dict(self) -> dict:
        return self._player_info_dict

    def get_player(self, player_name: str) -> Player:
        if not player_name in self.get_player_info_dict():
            raise ValueError("시스템에 등록되지 않은 player")
        return self.get_player_info_dict().get(player_name)

    def update_attendance_for_player(self, idx: int, player_name: str, day: str):
        if not day in [elem.value for elem in Weekday]:
            raise ValueError("유효 하지 않은 요일이 입력됨.")

        if player_name not in self._player_info_dict:
            self._player_info_dict[player_name] = Player(player_id = idx, name = player_name)

        player : Player= self._player_info_dict.get(player_name)
        player.attend(day= day)

    def calculate_score_and_grade(self):
        for player_name in self.get_player_info_dict():
            self.calculate_score_for_player(player_name)
            self.calculate_grade_for_player(player_name)

    def print_all_player_status(self):
        sorted_player_name_by_id = sorted(self.get_player_info_dict().items(), key=lambda x: x[1].id)
        for player_name, player in sorted_player_name_by_id:
            points = player.score
            grade = player.grade

            print(f"NAME : {player_name}, POINT : {points}, GRADE : {grade.value}", )

        print("\nRemoved player")
        print("==============")
        for player_name, _ in sorted_player_name_by_id:
            if self.check_remove_player(player_name):
                print(player_name)

    def check_remove_player(self, player_name: str):
        player: Player = self.get_player(player_name)
        if player.grade != Grade.NORMAL:
            return False
        if player.is_attend_on_wed_or_weekend():
            return False
        return True

    def calculate_score_for_player(self, player_name: str):
        player = self.get_player(player_name)
        total_score = 0
        for day, counts in player.get_attendance_counts().items():
            self._score_calculator.set_strategy(get_score_strategy_from_day(day))
            total_score += self._score_calculator.calculate(counts)

        self._score_calculator.set_bonus_strategy(get_bonus_strategy())
        total_score += self._score_calculator.calculate_bonus(player)

        player.score = total_score

    def calculate_grade_for_player(self, player_name: str):
        player = self.get_player(player_name)
        self._grade_calculator.set_strategy(get_grade_strategy())
        grade = self._grade_calculator.calculate(player.score)
        player.grade = grade




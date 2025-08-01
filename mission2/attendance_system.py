from mission2.day import Weekday
from mission2.default_score_strategy import DefaultScoreStrategy
from mission2.grade import Grade
from mission2.player import Player
from mission2.score_calculator import ScoreCalculator, get_strategy_from_day


class AttendanceSystem:
    def __init__(self):
        self._player_info_dict = dict()
        self._score_calculator = ScoreCalculator(strategy= DefaultScoreStrategy())

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
        sorted_player_name_by_id = sorted(self.get_player_info_dict().items(), key=lambda x: x[1].get_id())
        for player_name, player in sorted_player_name_by_id:
            points = player.get_score()
            grade = player.get_grade()

            print(f"NAME : {player_name}, POINT : {points}, GRADE : {grade.value}", )

        print("\nRemoved player")
        print("==============")
        for player_name, _ in sorted_player_name_by_id:
            if self.check_remove_player(player_name):
                print(player_name)

    def check_remove_player(self, player_name: str):
        player: Player = self.get_player(player_name)
        if player.get_grade() != Grade.NORMAL:
            return False
        if player.is_attend_on_wed_or_weekend():
            return False
        return True

    def calculate_score_for_player(self, player_name: str):
        player = self.get_player(player_name)
        for day, counts in player.get_attendance_counts().items():
            self._score_calculator.set_strategy(get_strategy_from_day(day))
            score = self._score_calculator.calculate(counts)
            player.add_score(score)
        self._add_bonus_for_player(player_name)

    def calculate_grade_for_player(self, player_name: str):
        player = self.get_player(player_name)
        if player.get_score() >= 50:
            player.set_grade(Grade.GOLD)
        elif player.get_score() >= 30:
            player.set_grade(Grade.SILVER)
        else:
            player.set_grade(Grade.NORMAL)


    def _add_bonus_for_player(self, player_name: str):
        player = self.get_player(player_name)
        bonus = 0
        if player.get_attendance_counts_per_day(Weekday.WEDNESDAY.value) >= 10:
            bonus += 10
        if player.get_attendance_counts_per_day(Weekday.SATURDAY.value) + \
                player.get_attendance_counts_per_day(Weekday.SUNDAY.value) >= 10:
            bonus += 10
        player.add_score(bonus)






from mission2.day import Weekday
from mission2.grade import Grade


class Player:
    def __init__(self, player_id: int, name: str):
        self._id = player_id
        self._name = name
        self._score = 0
        self._grade = Grade.NORMAL
        self._attend_counts = dict()

    def attend(self, day:str):
        if not day in self._attend_counts:
            self._attend_counts[day] = 0

        self._attend_counts[day] += 1

    def is_attend_on_wed_or_weekend(self):
        counts_wed = self._attend_counts.get(Weekday.WEDNESDAY.value, 0)
        counts_weekend = self._attend_counts.get(Weekday.SATURDAY.value, 0) + self._attend_counts.get(Weekday.SUNDAY.value, 0)
        return counts_wed + counts_weekend > 0

    def get_attendance_counts(self):
        return self._attend_counts

    def get_attendance_counts_per_day(self, day: str):
        return self._attend_counts.get(day, 0)

    def add_score(self, score: int):
        self._score += score

    def get_score(self):
        return self._score

    def get_grade(self):
        return self._grade

    def set_grade(self, grade: Grade):
        self._grade = grade

    def get_id(self):
        return self._id

import pytest

from mission2.day import Weekday
from mission2.player import Player


def test_attend_월요일3번출석():
    player = Player(player_id= 1, name= "홍길동")
    attend_day =  Weekday.MONDAY.value

    player.attend(day=attend_day)
    player.attend(day=attend_day)
    player.attend(day=attend_day)

    assert player.get_attendance_counts_per_day(attend_day) == 3

def test_is_attend_on_wed_or_weekend_월요일목요일출석_RETURN_FALSE():
    player = Player(player_id=1, name="홍길동")

    player.attend(day=Weekday.MONDAY.value)
    player.attend(day=Weekday.THURSDAY.value)

    assert player.is_attend_on_wed_or_weekend() == False

def test_is_attend_on_wed_or_weekend_수요일만2번_RETURN_TRUE():
    player = Player(player_id=1, name="홍길동")

    player.attend(day=Weekday.WEDNESDAY.value)
    player.attend(day=Weekday.WEDNESDAY.value)

    assert player.is_attend_on_wed_or_weekend() == True

def test_is_attend_on_wed_or_weekend_월요일1번토요일1번_RETURN_TRUE():
    player = Player(player_id=1, name="홍길동")

    player.attend(day=Weekday.MONDAY.value)
    player.attend(day=Weekday.SATURDAY.value)

    assert player.is_attend_on_wed_or_weekend() == True
    
def test_add_score():
    player = Player(player_id=1, name="홍길동")

    player.add_score(5)
    assert player.get_score() == 5

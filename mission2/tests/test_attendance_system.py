import pytest
import sys, io

from mission2.attendance_system import AttendanceSystem
from mission2.day import Weekday
from mission2.grade import Grade
from mission2.player import Player

def test_get_player_info_dict():
    input_data_list = [
        (1, "홍길동", Weekday.MONDAY.value),
        (2, "이순신", Weekday.WEDNESDAY.value)
    ]
    sut = AttendanceSystem()
    for idx, name, day in input_data_list:
        sut.update_attendance_for_player(idx=idx, player_name=name, day=day)

    assert "홍길동" in sut.get_player_info_dict()
    assert "이순신" in sut.get_player_info_dict()

def test_update_attendance_for_player_유효하지않은요일입력_RAISE_ERROR():
    sut = AttendanceSystem()

    with pytest.raises(ValueError):
        sut.update_attendance_for_player(idx= 1, player_name= "홍길동", day = "nonexistent_day")

@pytest.mark.parametrize("input_day_list, expected_status",[
    ([Weekday.MONDAY.value, Weekday.WEDNESDAY.value], True),
    ([Weekday.MONDAY.value, Weekday.MONDAY.value, Weekday.TUESDAY.value], False)
])
def test_update_attendance_for_player_월요일1번수요일한번씩참석(input_day_list, expected_status):
    player_name = "홍길동"
    sut = AttendanceSystem()
    for idx, day in enumerate(input_day_list):
        sut.update_attendance_for_player(idx=idx, player_name=player_name, day=day)

    player: Player = sut.get_player(player_name)
    assert player.is_attend_on_wed_or_weekend() == expected_status

@pytest.mark.parametrize("input_day_list, expected_result", [
    ([Weekday.WEDNESDAY.value] * 10 + [Weekday.SATURDAY.value] * 10, (70, Grade.GOLD)),
    ([Weekday.MONDAY.value] * 5 + [Weekday.WEDNESDAY.value] * 10, (45, Grade.SILVER)),
    ([Weekday.MONDAY.value] * 2 + [Weekday.WEDNESDAY.value, Weekday.SATURDAY.value, Weekday.SUNDAY.value], (9, Grade.NORMAL) ),
    ([Weekday.MONDAY.value, Weekday.MONDAY.value, Weekday.WEDNESDAY.value], (5, Grade.NORMAL))
])
def test_calculate_score_and_grade(input_day_list, expected_result):
    # Arrange
    player_name = "홍길동"
    sut = AttendanceSystem()
    for idx, day in enumerate(input_day_list):
        sut.update_attendance_for_player(idx=idx, player_name=player_name, day=day)
    # Act
    sut.calculate_score_and_grade()

    # Assert
    player = sut.get_player(player_name)
    assert player.get_score() == expected_result[0]
    assert player.get_grade() == expected_result[1]

def test_get_player_시스템에등록되지않은PLAYER():
    player_name = "홍길동"
    input_data_list = [
        (1, player_name, Weekday.MONDAY.value),
        (2, player_name, Weekday.WEDNESDAY.value)
    ]
    sut = AttendanceSystem()
    for idx, name, day in input_data_list:
        sut.update_attendance_for_player(idx=idx, player_name=name, day=day)

    with pytest.raises(ValueError):
        sut.get_player("아무개")

@pytest.mark.parametrize("input_day_list, expected_score", [
    ([Weekday.WEDNESDAY.value] * 10 + [Weekday.SATURDAY.value] * 10, 70),
    ([Weekday.MONDAY.value] * 5 + [Weekday.WEDNESDAY.value] * 10, 45),
    ([Weekday.MONDAY.value] * 2 + [Weekday.WEDNESDAY.value, Weekday.SATURDAY.value, Weekday.SUNDAY.value], 9 ),
    ([Weekday.MONDAY.value, Weekday.MONDAY.value, Weekday.WEDNESDAY.value], 5)
])
def test_set_score_for_player(input_day_list, expected_score):
    # Arrange
    player_name = "홍길동"
    sut = AttendanceSystem()
    for idx, day in enumerate(input_day_list):
        sut.update_attendance_for_player(idx=idx, player_name=player_name, day=day)
    # Act
    sut.calculate_score_for_player(player_name)

    # Assert
    player = sut.get_player(player_name)
    assert player.get_score() == expected_score

@pytest.mark.parametrize("score, expected_grade", [
    (50, Grade.GOLD), (30, Grade.SILVER), (10, Grade.NORMAL)
])
def test_get_grade_for_player(mocker, score, expected_grade):
    # Arrange
    player_name = "홍길동"
    player = Player(player_id=1, name=player_name)
    player.add_score(score)

    sut = AttendanceSystem()
    mocker.patch.object(sut, "get_player", return_value = player)

    # Act
    sut.calculate_grade_for_player(player_name= player_name)

    # Assert
    assert player.get_grade() == expected_grade

def test_print_all_player_status(mocker, capfd):
    # Arrange
    player_1 = Player(1, "홍길동")
    player_2 = Player(2,  "이순신")
    player_info_dict = {
        "홍길동" : player_1,
        "이순신": player_2
    }

    mocker.patch.object(player_1, "get_score", return_value = 50)
    mocker.patch.object(player_1, "get_grade", return_value = Grade.GOLD)
    mocker.patch.object(player_1, "is_attend_on_wed_or_weekend", return_value = True)

    mocker.patch.object(player_2, "get_score", return_value = 5)
    mocker.patch.object(player_2, "get_grade", return_value = Grade.NORMAL)
    mocker.patch.object(player_2, "is_attend_on_wed_or_weekend", return_value = False)

    sut = AttendanceSystem()
    mocker.patch.object(sut, "get_player_info_dict", return_value=player_info_dict)

    # Act
    sut.print_all_player_status()
    out, _ = capfd.readouterr()

    assert out == ('NAME : 홍길동, POINT : 50, GRADE : GOLD\n'
     'NAME : 이순신, POINT : 5, GRADE : NORMAL\n'
     '\n'
     'Removed player\n'
     '==============\n'
     '이순신\n')

@pytest.mark.parametrize("grade, attend_status, expected_result", [
    (Grade.NORMAL, False, True), (Grade.NORMAL, True, False), (Grade.GOLD, False, False)
])
def test_check_remove_player(mocker, grade, attend_status, expected_result):
    # Arrange
    player_name = "홍길동"
    player = Player(1, player_name)

    mocker.patch.object(player, "get_grade", return_value = grade)
    mocker.patch.object(player, "is_attend_on_wed_or_weekend", return_value = attend_status)

    sut = AttendanceSystem()
    mocker.patch.object(sut, "get_player", return_value = player)

    # Act
    result = sut.check_remove_player(player_name= player_name)

    # Assert
    assert result == expected_result
NORMAL = "NORMAL"
SILVER = "SILVER"
GOLD = "GOLD"
GRADE = "grade"
ATTEND_COUNTS = "attend_counts"
ATTEND_ON_WEEKEND = "is_attend_on_weekend"
ATTEND_ON_WED = "is_attend_on_wed"
POINTS = "points"
PLAYER_ID = "id"

SUNDAY = "sunday"
SATURDAY = "saturday"
FRIDAY = "friday"
THURSDAY = "thursday"
WEDNESDAY = "wednesday"
TUESDAY = "tuesday"
MONDAY = "monday"


def make_player_info(player_id: int, player_name: str, day: str, all_player_info_dict: dict):
    if not day in [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]:
        print("유효 하지 않은 요일이 입력됨.")
        return

    if player_name not in all_player_info_dict:
        all_player_info_dict[player_name] = {
            PLAYER_ID: player_id,
            POINTS: 0,
            ATTEND_ON_WED: False,
            ATTEND_ON_WEEKEND: False,
            ATTEND_COUNTS: {MONDAY:0, TUESDAY:0, WEDNESDAY:0, THURSDAY:0, FRIDAY:0, SATURDAY:0, SUNDAY:0}
        }

    if day == WEDNESDAY:
        add_points = 3
        all_player_info_dict[player_name][ATTEND_ON_WED] = True
    elif day == SATURDAY or day == SUNDAY:
        add_points = 2
        all_player_info_dict[player_name][ATTEND_ON_WEEKEND] = True
    else:
        add_points = 1

    all_player_info_dict[player_name][POINTS] += add_points
    all_player_info_dict[player_name][ATTEND_COUNTS][day] += 1

def make_final_points_and_grade(all_player_info_dict: dict):
    for play_name, player_info in all_player_info_dict.items():
        player_info[POINTS] += get_bonus(player_info)
        player_info[GRADE] = get_grade(player_info)

def get_bonus(player_info: dict):
    bonus = 0
    if player_info[ATTEND_COUNTS][WEDNESDAY] >= 10:
        bonus += 10
    if player_info[ATTEND_COUNTS][SATURDAY] + player_info[ATTEND_COUNTS][SUNDAY] >= 10:
        bonus += 10
    return bonus

def get_grade(player_info: dict):
    if player_info[POINTS] >= 50:
        return GOLD
    if player_info[POINTS] >= 30:
        return SILVER
    return NORMAL

def read_input_file(file_path : str):
    try:
        data = []
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    data.append(parts)
        return data
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def print_result(all_player_info_dict : dict):
    sorted_player_name_by_id = sorted(all_player_info_dict.items(), key=lambda player: player[1][PLAYER_ID])

    for player_name, player_info in sorted_player_name_by_id:
        points = player_info.get(POINTS)
        grade = player_info.get(GRADE)
        print(f"NAME : {player_name}, POINT : {points}, GRADE : {grade}",)

    print("\nRemoved player")
    print("==============")
    for player_name, player_info in sorted_player_name_by_id:
        if is_removed_player(player_info):
            print(player_name)


def is_removed_player(player_info : dict):
    if player_info[GRADE] == NORMAL and \
            (player_info[ATTEND_ON_WED] == False and player_info[ATTEND_ON_WEEKEND] == False):
        return True
    return False

def run():
    input_file_path = "attendance_weekday_500.txt"
    input_data = read_input_file(file_path = input_file_path)
    all_player_info_dict = dict()
    for idx, parts in enumerate(input_data):
        make_player_info(player_id= idx, player_name= parts[0], day= parts[1], all_player_info_dict= all_player_info_dict)
    make_final_points_and_grade(all_player_info_dict= all_player_info_dict)
    print_result(all_player_info_dict= all_player_info_dict)

if __name__ == "__main__":
    run()

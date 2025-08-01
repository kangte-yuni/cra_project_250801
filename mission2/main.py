from mission2.attendance_system import AttendanceSystem


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

def run():
    input_file_path = "attendance_weekday_500.txt"
    input_data = read_input_file(file_path = input_file_path)
    attend_system = AttendanceSystem()

    for idx, parts in enumerate(input_data):
        attend_system.update_attendance_for_player(idx = idx, player_name = parts[0], day = parts[1])

    attend_system.calculate_score_and_grade()
    attend_system.print_all_player_status()

if __name__ == "__main__":
    run()
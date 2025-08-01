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
    print(input_data)
    # all_player_info_dict = dict()
    # for idx, parts in enumerate(input_data):
    #     make_player_info(player_id= idx, player_name= parts[0], day= parts[1], all_player_info_dict= all_player_info_dict)
    # make_final_points_and_grade(all_player_info_dict= all_player_info_dict)
    # print_result(all_player_info_dict= all_player_info_dict)

if __name__ == "__main__":
    run()
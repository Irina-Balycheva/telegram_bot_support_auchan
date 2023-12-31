import json
import os
from datetime import datetime


class json_for_logs():
    LOCAL_DIRECTORY_LOGS = f'{os.getcwd()}/database/logs'

    def write_data(self, data, id_user='id_user', title=LOCAL_DIRECTORY_LOGS):
        with open(f"{title}_{id_user}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, default=str, ensure_ascii=False)

    def load_data_all(self, title=LOCAL_DIRECTORY_LOGS):
        with open(f"{title}.json", "r") as file:
            data = json.load(file)
        return data

    def merge_data(self, new_data_json=None, id_user='id_user', title=LOCAL_DIRECTORY_LOGS):
        try:
            with open(f"{title}_{id_user}.json", "r") as json_file:
                data = json.load(json_file)

            for new_data in new_data_json[id_user]:
                data[id_user].append(new_data)

            with open(f"{title}_{id_user}.json", "w") as json_file:
                json.dump(data, json_file, default=str, ensure_ascii=False, indent=4)

            # print("Данные успешно добавлены в JSON файл:", title)
        except Exception as e:
            print('Ошибка! Идет перезапись БД. Тип ошибки:', e)
            self.write_data(data=new_data_json, id_user=id_user, title=title)

    # Подсчет общее время
    def calculate_dialogue_duration(self, data_json):
        duration_json = {}
        # Подсчет и вывод общего времени для каждого диалога
        for user_id, dialogues in data_json.items():
            duration_list = []
            for dialogue in dialogues:
                if len(dialogue) < 2:
                    duration_list.append(None)

                start_time = datetime.strptime(dialogue[0]['datetime'], "%Y-%m-%d %H:%M:%S.%f")
                end_time = datetime.strptime(dialogue[-1]['datetime'], "%Y-%m-%d %H:%M:%S.%f")
                duration = (end_time - start_time).total_seconds()

                if duration is not None:
                    print(f"ID пользователя: {user_id}, Длительность диалога: {duration} секунд")

                duration_list.append(duration)
            duration_json[user_id] = duration_list

        return duration_json

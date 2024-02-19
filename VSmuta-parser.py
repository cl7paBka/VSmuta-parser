import json
import requests

date = input("Введите дату в формате YEAR-MM-DD: ")
link = 'https://vsmuta.com/api/logs/blood/'
response = requests.get(link+date)
if response.status_code == 200:
    data = json.loads(response.text)
    if data['status'] == 'success':
        battles = data['battles']
        winners_counter = len(battles)
        losers_counter = len(battles)
        clans_counter = dict()

        for battle in battles:
            for member in battle['members']:
                clan = member['clan']
                clans_counter.setdefault(clan, [0, 0]) #Первое значение списка - победы, второе поражения
                if member['team'] == 1:
                    clans_counter[clan][0] += 1
                else:
                    clans_counter[clan][1] += 1


        print(f"Количество игроков: {winners_counter+losers_counter}\n"
              f"Количество кланов: {len(clans_counter)}\n"
              f"Кланы:\n")
        for clan in clans_counter:
            print(clan)

#2024-02-19

    else:
        print(f"Error: {data['message']}")
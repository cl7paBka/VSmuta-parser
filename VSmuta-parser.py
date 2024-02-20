import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('Date', type=str,
                    help='Input day in this format: YYYY-MM-DD')
args = parser.parse_args()

date = args.Date
link = 'https://vsmuta.com/api/logs/blood/'
response = requests.get(link + date)
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
                clans_counter.setdefault(clan, [0, 0])  # Первое значение списка - победы, второе поражения
                if member['team'] == 1:
                    clans_counter[clan][0] += 1
                else:
                    clans_counter[clan][1] += 1

        print(f"Количество игроков: {winners_counter + losers_counter}\n"
              f"Количество кланов: {len(clans_counter)}\n"
              f"Кланы:")
        for clan in clans_counter:
            print(f"{clan}\n"
                  f"Победы: {clans_counter[clan][0]}\n"
                  f"Поражения: {clans_counter[clan][1]}\n")


    else:
        print(f"Error: {data['message']}")

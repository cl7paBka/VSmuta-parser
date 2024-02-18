import json
import requests
from pprint import pprint

link = 'https://vsmuta.com/api/logs/blood/2024-02-17'
response = requests.get(link)
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
                clans_counter.setdefault(clan, [0, 0])
                if member['team'] == 1:
                    clans_counter[clan][0] += 1
                else:
                    clans_counter[clan][1] += 1

        pprint(clans_counter)
        print(winners_counter)
        print(losers_counter)

    else:
        print(f"Error: {data['message']}")
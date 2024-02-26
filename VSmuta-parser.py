import json
import argparse
import requests


def parse_args():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('Date', type=str,
                        help='Input day in this format: YYYY-MM-DD')
    parser.add_argument('-o', '--output', type=str,
                        help='If you want to save the output to .txt file, type filepath here')
    args = parser.parse_args()


def saving_output(output_path, output):
    if output_path is not None:
        with open(output_path, 'w') as output_file:
            output_file.writelines(output)
        print(f"Output saved to {args.output}")


def run():
    date = args.Date
    link = 'https://vsmuta.com/api/logs/blood/'
    response = requests.get(link + date)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['status'] == 'success':
            battles = data['battles']
            players_counter = 0
            clans_counter = dict()

            for battle in battles:
                for member in battle['members']:
                    players_counter += 1
                    player_name = member['title']
                    clan = member['clan']
                    clans_counter.setdefault(clan, {'players': set(), 'wins': 0, 'losses': 0})
                    clans_counter[clan]['players'].add(player_name)
                    if member['team'] == 1:
                        clans_counter[clan]['wins'] += 1
                    else:
                        clans_counter[clan]['losses'] += 1
            day_information = (f"День: {date}\n"
                               f"Количество игроков: {players_counter}\n"
                               f"Количество кланов: {len(clans_counter)}\n"
                               f"Кланы: \n")

            for clan in clans_counter:
                day_information += (f"{'_' * 30}\n"
                                    f"• {clan}\n"
                                    f"Победы: {clans_counter[clan]['wins']}\n"
                                    f"Поражения: {clans_counter[clan]['losses']}\n"
                                    f"Игроки: {' | '.join(name for name in clans_counter[clan]['players'])}\n"
                                    f"{'_' * 30}\n")
            print(day_information)
            return day_information


        else:
            print(f"Error: {data['message']}")


def main():
    parse_args()
    output = run()
    saving_output(args.output, output)


if __name__ == '__main__':
    main()

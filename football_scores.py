import pip._vendor.requests as requests
import json
from datetime import datetime, time
import time
import os

today = datetime.today().strftime('%Y%m%d')


# today = '20221001'

def showing_games(choice, jsondata):
    for game in jsondata['events']:
        teams = game['name']
        ascore = game['competitions'][0]['competitors'][1]['score']
        hscore = game['competitions'][0]['competitors'][0]['score']
        status = game['status']['type']['detail']
        if game['status']['type']['description'] == "Scheduled" and choice == 'live':
            continue
        elif game['status']['type']['description'] == "Scheduled" and choice == 'all':
            print(f'{teams} | {status}')
            continue
        if game['status']['type']['description'] == "Final" and choice == 'live':
            continue
        elif game['status']['type']['description'] == "Final" and choice == 'all':
            print(f'{teams} | {ascore}-{hscore} | {status}')
            continue
        try:
            if game['competitions'][0]['competitors'][0]['id'] == game['competitions'][0]['situation']['possession']:
                print(
                    f"{teams} | {ascore}-{hscore} | {status} | {game['competitions'][0]['situation']['downDistanceText']}, {game['competitions'][0]['competitors'][0]['team']['location']} ball")
            elif game['competitions'][0]['competitors'][1]['id'] == game['competitions'][0]['situation'][
                'possession']:
                print(
                    f"{teams} | {ascore}-{hscore} | {status} | {game['competitions'][0]['situation']['downDistanceText']}, {game['competitions'][0]['competitors'][1]['team']['location']} ball")
        except KeyError:
            try:
                print(
                    f"{teams} | {ascore}-{hscore} | {status} | {game['competitions'][0]['situation']['lastPlay']['text']}")
            except KeyError:
                print(f"{teams} | {ascore}-{hscore} | {status} | This game is live")


def scoreboard():
    os.system("clear")
    while True:
        league = input("Which league do you want? NFL/college: ").lower()
        if league in ['nfl', 'college']:
            break
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'site.api.espn.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
    }
    if league == 'college':
        urlline = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={today}&limit=200'
    elif league == 'nfl':
        urlline = f'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    while True:
        choice = input("Which games do you want? all/live: ")
        if choice in ['all', 'live']:
            break
    while choice == 'live':
        response = requests.request("GET", urlline, headers=headers)
        jsondata = json.loads(response.text)
        showing_games(choice, jsondata)
        print('\n')
        time.sleep(5)
        os.system("clear")
    if choice == 'all':
        response = requests.request("GET", urlline, headers=headers)
        jsondata = json.loads(response.text)
        showing_games(choice, jsondata)


if __name__ == '__main__':
    scoreboard()

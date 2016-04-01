import sys
import time
import datetime
import random
import datetime
import telepot
import requests
import json

"""
A simple bot that provides data about Warriors schedule & resutls.
- /dubs : reply with Warriors info

$ python dylbot.py

Ctrl-C to kill.

Based on diceyclock example from the telepot library.
"""
config = {
    'telegramToken' : '<insert token>',
    'xmlstatsAuthToken' : '<insert token>',
    'dubsName' : 'Golden State Warriors',
    'dubsCity' : 'Oakland',
    'lalName' : 'Los Angeles Lakers',
    'lalCity' : 'Los Angeles',
    'sasName' : 'San Antonio Spurs',
    'sasCity' : 'San Antonio',
}

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command.startswith('/dubs'): # direct message
        bot.sendMessage(chat_id, getTeamData(getConfig('dubsName'), getConfig('dubsCity')),  parse_mode='Markdown')
    elif command.startswith('/lakers'):
        bot.sendMessage(chat_id, getTeamData(getConfig('lalName'), getConfig('lalCity')),  parse_mode='Markdown')
    elif command.startswith('/spurs'):
        bot.sendMessage(chat_id, getTeamData(getConfig('sasName'), getConfig('sasCity')),  parse_mode='Markdown')
    else:#if command == '/dubs':
        bot.sendMessage(chat_id, "Unknown command: " + command)

def getConfig(key):
    return config[key]

def getRecord(allStandings, teamName):
    team = teamName.replace(' ', '-').lower()
    for x in allStandings:
        if x['team_id'] == team:
            gamesWon = x['won']
            gamesLost = x['lost']
    return '(' + str(gamesWon) + '-' + str(gamesLost) + ')'

def getTeamData(team, city):
    today = time.localtime()
    teamName = team.replace(' ', '-').lower()
    teamCity = city

    # Get current standings from https://erikberg.com/nba/standings.json
    gamesWon = 0
    gamesLost = 0
    lastTen = ""
    headers = {'user-agent': 'nbabot/0.1 (marketing@doliver.net)'}
    r = requests.get('https://erikberg.com/nba/standings.json', headers=headers)
    print 'Standings url: ' + r.url
    content = json.loads(r.text)
    standingList = content['standing']
    for x in standingList:
        if x['team_id'] == teamName:
            gamesWon = x['won']
            gamesLost = x['lost']
            lastTen = x['last_ten']
    strRec = str(gamesWon) + '-' + str(gamesLost) + "  _(Last 10 games: " + lastTen + ")_"

    # Get previous game from https://erikberg.com/nba/results/golden-state-warriors.json
    prevStr = 'xxx'
    headers = {'user-agent': 'dubsbot/0.1 (marketing@doliver.net)', 'Authorization': getConfig('xmlstatsAuthToken')}
    payload = {'since' : '20160315', 'until' : (datetime.datetime(*today[:6])).strftime("%Y%m%d")}
    r = requests.get('https://erikberg.com/nba/results/'+teamName+'.json', headers=headers, params=payload)
    print 'Previous game url: ' + r.url
    content = json.loads(r.text)
    g = content[0]
    result = 'W' if g['team_event_result'] == 'win' else 'L'
    gswPts = g['team_points_scored']
    oppPts = g['opponent_points_scored']
    opponent = g['opponent']['last_name']
    location = ' vs. ' if g['site']['city'] == teamCity else ' @ '
    strPrev = result + ' ' + str(gswPts) + ' - ' + str(oppPts) + location + opponent

    # Get upcoming games from SeatGeek
    payload = {'performers.slug' : teamName, 'datetime_utc.gt' : (datetime.datetime(*today[:6])).strftime("%Y-%m-%d")}
    r = requests.get('https://api.seatgeek.com/2/events', params=payload)
    print 'Upcoming games url: ' + r.url
    content = json.loads(r.text)
    eventList = content['events']
    strUpcoming="";
    for x in range(0, len(eventList)):
        if len(eventList[x]['performers']) < 2:    # hack to avoid TBD playoff data at the end of this list
            continue
        gt = time.strptime(eventList[x]['datetime_local'], "%Y-%m-%dT%H:%M:%S")
        gametime = datetime.datetime(*gt[:6])
        location = ' vs. '  if eventList[x]['venue']['city'] == teamCity else ' @ '
        opponent = eventList[x]['performers'][0]['name'] if eventList[x]['performers'][1]['slug'] == teamName else eventList[x]['performers'][1]['name']
        record = ' ' + getRecord(standingList, opponent)
        strUpcoming += gametime.strftime("%m/%d") + location + opponent + record + '\n'

    return "*Current record:* " + strRec + \
        "\n*Previous game:* " + strPrev + "\n" + \
        "\n*Upcoming games:*\n" + strUpcoming

bot = telepot.Bot(getConfig('telegramToken'))
bot.notifyOnMessage(handle)
print 'ready & waiting ...'

while 1:
    time.sleep(10)

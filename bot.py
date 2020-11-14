import http.client
import config
import logging
import json
import requests

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level = logging.INFO)

bot = Bot(token = config.API_TOKEN_TG_BOT)
dp = Dispatcher(bot)

strAPI = config.API_TOKEN_DATA

class requestHandler(object):
    LIVE_URL = 'http://soccer-cli.appspot.com/'

def live_scores():
    req = requests.get(requestHandler.LIVE_URL)
    print(req)

    if req.status_code == requests.codes.ok:
        scores_data = []
        scores = req.json()
        if len(scores["games"]) == 0:
            print('no live action currently')
            return 'no live action currently'
        else:

            for score in scores['games']:
                d = {}

                d['homeTeam'] = {'name': score['homeTeamName']}
                d['awayTeam'] = {'name': score['awayTeamName']}

                d['score'] = {'fullTime': {'homeTeam': score['goalsHomeTeam'], 'awayTeam': score['goalsAwayTeam']}}
                d['league'] = score['league']
                d['time'] = score['time']
                
                scores_data.append(d)
                print(scores_data)
                result = scores_data
                return result
    else:
        return 'live server dead'

def gogo():
    print('log2')
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = { 'X-Auth-Token': strAPI }
    connection.request('GET', '/v2/competitions/DED', None, headers )
    response = json.loads(connection.getresponse().read().decode())

    resultStr = response
    print (response)
    return resultStr



@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'hello' or message.text == 'Hello':
        message.text = 'Hello'
        await message.answer(message.text)

    elif message.text == 'привет' or message.text == 'Привет':
        message.text = 'Привет'
        await message.answer(message.text)

    elif message.text == 'live' or message.text == 'Live':
        str = live_scores()
        message.text = str
        await message.answer(message.text)

    elif message.text == 'fuck' or message.text == 'Fuck':
        print('log1')
        str = gogo()
        message.text = str
        await message.answer(message.text)

    else:
        print('log ELSE')
        message.text = 'log Else'
        await message.answer(message.text)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

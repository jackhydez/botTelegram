#import http.client
import config
import logging

import json
import requests

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level = logging.INFO)

bot = Bot(token = config.API_TOKEN_TG_BOT)
dp = Dispatcher(bot)

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
                result = string(scores_data)
                return result
    else:
        return 'Сервер не отвечает'


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'hello' or message.text =='Hello':
        message.text = 'Hello'
        await message.answer(message.text)

    if message.text == 'привет' or message.text =='Привет':
        message.text = 'Привет'
        await message.answer(message.text)

    if message.text == 'live' or 'Live':
        str = live_scores()
        message.text = str
        await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

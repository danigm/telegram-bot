#!/usr/bin/env python

import time
import requests


class DGMBot:
    def __init__(self):
        self.token = open('token').read().split()[0]
        self.api = 'https://api.telegram.org/bot%s/' % self.token
        self.offset = int(open('offset').read().split()[0])
        self.me = self.botq('getMe')

    def botq(self, method, params=None):
        url = self.api + method
        params = params if params else {}
        return requests.post(url, params).json()

    def updates(self):
        print("updating")
        data = {'offset': self.offset}
        r = self.botq('getUpdates', data)
        for up in r['result']:
            print(up['message'])
            self.reply(up['message']['chat']['id'], up['message']['text'])
            self.offset = up['update_id']
            self.offset += 1
        open('offset', 'w').write('%s' % self.offset)

    def reply(self, to, msg):
        resp = self.botq('sendMessage', {'chat_id': to, 'text': msg})
        return resp

    def run(self):
        while True:
            self.updates()
            time.sleep(1)


if __name__ == '__main__':
    bot = DGMBot()
    bot.run()

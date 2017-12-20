from wxpy import *
from apscheduler.schedulers.background import BackgroundScheduler
import time, os
import urllib, json
import itertools
import shutil


class BBer:
    tail = " ".rjust(26)
    Log_path = "./Log"
    history_path = "./history"

    def __init__(self, time, toGroups=None, toFriends=None):
        self.bot = Bot(cache_path=True)
        self.toGroups = self.search_friends(toFriends)
        self.toFriends = self.search_groups(toGroups)
        self.show_receivers(self.toFriends + self.toGroups)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.reportTo, 'cron', **time, id="dailyReport", misfire_grace_time=30)
        self.scheduler.start()

    def search_friends(self, names):
        if names is None: return []
        friends = self.bot.friends()
        return list(itertools.chain(*[friends.search(name) for name in names]))

    def search_groups(self, names):
        if names is None: return []
        groups = self.bot.groups()
        return list(itertools.chain(*[groups.search(name, None, nick_name=name) for name in names]))

    def reportTo(self):
        msg = self.get_message()
        if len(msg):
            message = f'{self.time_weather()}\n\n{msg}\n{self.tail}'
            for name in self.toGroups + self.toFriends:
                name.send(message)

    def time_weather(self):
        timestamp = time.strftime('%Y-%m-%d %a', time.localtime(time.time()))
        url = "http://weixin.jirengu.com/weather/now?cityid=WTW3SJ5ZBJUY"
        weather = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        weather = "" if weather['status'] != 'OK' else weather['weather'][0]['now']['temperature'] + '℃ ' + \
                                                       weather['weather'][0]['now']['text']
        return "{} {}".format(timestamp, weather)

    def get_message(self):
        msg_file = os.listdir(self.Log_path)
        if len(msg_file) == 0: return ""
        msg_file = os.path.join(self.Log_path, msg_file[0])
        with open(msg_file, 'r', encoding='utf-8') as f:
            message = '\n'.join(map(lambda line: line.strip(), f.readlines()))
        # os.remove(msg_file)
        shutil.move(msg_file, self.history_path)
        return message

    def show_receivers(self, receivers):
        print(receivers)

if __name__ == "__main__":
    BBer(time={"hour": 23, "minute": 59}, toFriends=["张加乘"], toGroups=["大j"])
    embed()

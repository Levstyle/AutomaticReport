from wxpy import *
from tinydb import TinyDB, Query
import arrow
from apscheduler.schedulers.background import BackgroundScheduler

bot, tuling = Bot(cache_path=True), Tuling(api_key='在此填入你的key')
# 去http://www.tuling123.com 申请你自己的api_key

friends, groups, reportTo = [], ["一个亿的策马奔腾"], ["一个亿的策马奔腾"]

scheduler = BackgroundScheduler()


def searchFriends(friend_names, type_name):
    friends = []
    for name in friend_names:
        if hasattr(bot, type_name):
            ret = getattr(bot, type_name)().search(name)
            if len(ret): friends.append(ret[0])
    return friends


def report():
    db = TinyDB('dailyReport.json')
    table = db.table(arrow.utcnow().to('local').format('YYYY-MM-DD')).all()
    if len(table) == 0:
        print(arrow.utcnow().to('local').format('YYYY-MM-DD H:M:S'), "发送日报失败")
        return

    table = table[0]
    contents = table["title"] + '\n' + table["contents"]
    for recipient in searchFriends(reportTo,"groups"):
        recipient.send(contents + "\n----------- 自动发报测试")
    print(arrow.utcnow().to('local').format('YYYY-MM-DD H:M:S'), "发送一次日报")


@bot.register(searchFriends(friends, "friends") + searchFriends(groups, "groups"), TEXT)
def auto_reply(msg):
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        msg.reply(tuling.reply_text(msg) + "\n---------------自动回复")


scheduler.add_job(report, 'cron', hour=18, minute=35, id="dailyReport")
scheduler.start()

embed()

if __name__ == "__main__":
    # report()
    pass




# AutomaticReport
一段代码片段，用来每天自动使用微信向老板发日报，搬砖真苦！
# 运行环境
建议使用Python3，Python2没测过

# 依赖
1. wxpy
2. arrow
3. tinydb
4. apscheduler
# 使用方法
- 使用insertDailyReport往文档型数据库中写入每天要准备发送的日报
- 使用scheduler.add_job中的hour 和 minute参数设置每天发送的日报时间，取值范围分别为[0,23],[0,59]
- 程序会自动读取对应日期的数据进行发送，如果没有对应日的数据，程序不会自行发送
- 如果要明天发送今天的日报，注意自行将日报时间减一

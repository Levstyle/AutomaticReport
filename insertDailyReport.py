from tinydb import TinyDB, Query
import arrow


def insertDailyReport(table_name, contents):
    db = TinyDB('dailyReport.json')
    table = db.table(table_name)
    if len(table.all()):
        db.purge_table(table_name)
        table = db.table(table_name)
    table.insert(contents)

if __name__ == "__main__":
    dailyReport = {
        "title": "2017-04-05",
        "contents": "1. 准备&参加组会\n2. 阅读发表在ICLR2017上的论文《Dynamic Coattention Networks For QA》\n3. 安装&配置TensorFlow"
    }
    insertDailyReport(arrow.utcnow().to('local').format('YYYY-MM-DD'), dailyReport)

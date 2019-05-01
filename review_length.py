# !/usr/bin/python
import pymysql
import matplotlib.pyplot as plt
from pylab import *
from config import DB_config, len_limit


class DB:
    def __init__(self):
        db_config = DB_config()
        self.db = pymysql.connect(user=db_config.user,
                            password=db_config.password,
                            port = db_config.port,
                            host=db_config.host,
                            db=db_config.db)
        self.cursor = self.db.cursor()
    
    def execute(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.db.commit()

        return result

    def close(self):
        self.db.close()


if __name__ == '__main__':
    db = DB()
    ll = len_limit()
    limit = ll.limit
    sql = "select CHAR_LENGTH(text) as review_len,(useful+funny+cool) as user_read " \
          "from review limit %d;"%limit
    result = db.execute(sql)
    db.close()

    review_length = [data[0] for data in result]
    user_read = [data[1] for data in result]

    statistic = np.zeros((2, 6))
    for data in result:
        for i in range(0,6):
            if 1000*i <= data[0] < 1000*(i+1):
                statistic[0][i] = statistic[0][i] + 1
                statistic[1][i] = statistic[1][i] + data[1]
    aver = statistic[1]/statistic[0]
    re_len = [0, 1000, 2000, 3000, 4000, 5000]
    plt.bar(re_len, aver, 1000, align='edge', color='rgb')
    plt.xlabel('review_length')
    plt.ylabel('average of user feedback')
    plt.title('user review')
    plt.show()

'''
    plt.figure(1)
    plt.plot(review_length, user_read, '*')
    ylim(0, 60)
    xlim(0, 7000)
    plt.title('user review')
    plt.xlabel('review_length')
    plt.ylabel('user feedback')
    plt.show()
'''
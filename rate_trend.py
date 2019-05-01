# !/usr/bin/python3
import pymysql
import matplotlib.pyplot as plt
from pylab import *
from scipy.signal import savgol_filter
from config import DB_config
from config import trend

class DB:
    def __init__(self):
        db_config = DB_config()
        self.db = pymysql.connect(user= db_config.user,
                            password=db_config.password,
                            port = db_config.port,
                            host=db_config.host,
                            db=db_config.db)
        self.cursor = self.db.cursor()
    
    def execute(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.db.close()


if __name__ == '__main__':
    db = DB()
    trend = trend()
    business_id = trend.business_id
    sql = "select date, avg(stars) from review where business_id = '%s' group by date order by date;" %business_id
    result = db.execute(sql)
    db.close()
    date_list = [data[0] for data in result]
    stars_list = [data[1] for data in result]
    rate_list = []
    sum = 0
    for num, rate in enumerate(stars_list):
        sum += rate
        avg = sum/(num + 1)
        rate_list.append(avg)
    #rate_list = savgol_filter(rate_list, 7, 1)
    plt.figure(1)
    plt.plot(date_list, rate_list)
    ylim(0, 6)
    plt.title('Rate Trending')
    plt.xlabel('date')
    plt.ylabel('average rate')
    plt.show()


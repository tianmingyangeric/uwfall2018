import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QLCDNumber, QSlider, QVBoxLayout, QHBoxLayout, QFrame, QSplitter,
                             QPushButton, QLineEdit, QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets,QtGui
from random import randint
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
#from config import DB_config,user_rate,trend,len_limit
import config
import os
import http.client


class DB_min(QWidget):
     
    def __init__(self):
        super().__init__()
        self.initUI()
         
         
    def initUI(self):
        #set up the main window

        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Data Mining')
    
        # Database configuration 
        db = config.DB_config()
        db_lbl = QLabel('DB config', self)
        db_lbl.move(20, 10)

        db_lbl = QLabel('user', self)
        db_lbl.move(20, 30)

        self.user_textbox = QLineEdit(db.user,self)
        self.user_textbox.move(100, 30)
        self.user_textbox.resize(100, 20)

        db_lbl = QLabel('password', self)
        db_lbl.move(20, 50)

        self.pwd_textbox = QLineEdit(db.password,self)
        self.pwd_textbox.move(100, 50)
        self.pwd_textbox.resize(100, 20)

        db_lbl = QLabel('port', self)
        db_lbl.move(20, 70)

        self.port_textbox = QLineEdit(str(db.port),self)
        self.port_textbox.move(100, 70)
        self.port_textbox.resize(100, 20)
        
        db_lbl = QLabel('host', self)
        db_lbl.move(20, 90)

        self.host_textbox = QLineEdit(db.host,self)
        self.host_textbox.move(100, 90)
        self.host_textbox.resize(100, 20)


        db_lbl = QLabel('database', self)
        db_lbl.move(20, 110)

        self.db_textbox = QLineEdit(db.db, self)
        self.db_textbox.move(100, 110)
        self.db_textbox.resize(100, 20)

        #user predict

        ur = config.user_rate()
        db_lbl = QLabel('User Predict', self)
        db_lbl.move(20, 150)

        db_lbl = QLabel('Bussiness Id', self)
        db_lbl.move(20, 170)

        self.bid_textbox = QLineEdit(ur.business_id, self)
        self.bid_textbox.move(100, 170)
        self.bid_textbox.resize(200, 20)

        db_lbl = QLabel('User Id', self)
        db_lbl.move(20, 190)

        self.uid_textbox = QLineEdit(ur.user_id, self)
        self.uid_textbox.move(100, 190)
        self.uid_textbox.resize(200, 20)


        #business trend
        br = config.trend()

        db_lbl = QLabel('Bussiness Trend', self)
        db_lbl.move(20, 230)

        db_lbl = QLabel('Bussiness Id', self)
        db_lbl.move(20, 250)

        self.Bid_textbox = QLineEdit(br.business_id,self)
        self.Bid_textbox.move(100, 250)
        self.Bid_textbox.resize(200, 20)

        #length limit 
        l_limit = config.len_limit()

        db_lbl = QLabel('Length Limit', self)
        db_lbl.move(20, 290)

        db_lbl = QLabel('Length Limit', self)
        db_lbl.move(20, 310)

        self.lid_textbox = QLineEdit(str(l_limit.limit),self)
        self.lid_textbox.move(120, 310)
        self.lid_textbox.resize(100, 20)

        save_btn = QPushButton('Save Configure', self)
        save_btn.resize(200, 40)
        save_btn.move(20, 350)
        save_btn.clicked.connect(self.reload_module)


        save_btn = QPushButton('Data Clean', self)
        save_btn.resize(200, 40)
        save_btn.move(20, 420)
        #save_btn.clicked.connect(self.connect_server)

        trend_btn = QPushButton('Business Trending', self)
        trend_btn.resize(200, 40)
        trend_btn.move(370, 30)
        trend_btn.clicked.connect(self.business_trend)

        pre_btn = QPushButton('Predict Rate', self)
        pre_btn.resize(200,40)
        pre_btn.move(370, 120)
        pre_btn.clicked.connect(self.predict_rate)


        hour_btn = QPushButton('Operation Hour', self)
        hour_btn.resize(200,40)
        hour_btn.move(370, 210)
        hour_btn.clicked.connect(self.operation_hour)


        review_btn = QPushButton('Review Length', self)
        review_btn.resize(200, 40)
        review_btn.move(370, 300)
        review_btn.clicked.connect(self.review_length)


        self.show()

    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, "Message", 'You typed:' + textboxValue, 
                             QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText('')

    def business_trend(self):
        os.system("python rate_trend.py")

    def predict_rate(self):
        url = "http://localhost:8080/?user=1"
        conn = http.client.HTTPConnection('localhost:8080')
        conn.request(method="GET", url=url)
        response = conn.getresponse()
        res = str(response.read())
        result = res.split("'")
        result = result[1]
        result = result.split(';')
        a = result[0]
        b = result[1]
        c = result[2]
        QMessageBox.information(self, "Result",  a+'\n'+b+'\n'+c)
        #self.resultLabel.setText("Information")

    def review_length(self):
        os.system("python review_length.py")

    def operation_hour(self):
        os.system("python rate_trend.py")

    def connect_server(self):
        os.system("python server.py")

    def reload_module(self):

        db = config.DB_config()
        self.alter("config.py","user='%s'" %db.user ,"user='%s'"%self.user_textbox.text())
        self.alter("config.py","password='%s'" %db.password ,"password='%s'"%self.pwd_textbox.text())
        self.alter("config.py","port=%s" %db.port ,"port=%s"%self.port_textbox.text())
        self.alter("config.py","host='%s'" %db.host ,"host='%s'"%self.host_textbox.text())
        self.alter("config.py","db='%s'" %db.db ,"db='%s'"%self.db_textbox.text())
        
        ur = config.user_rate()
        self.alter("config.py","business_id = '%s'" %ur.business_id ,"business_id = '%s'"%self.bid_textbox.text())
        self.alter("config.py","user_id = '%s'" %ur.user_id ,"user_id = '%s'"%self.uid_textbox.text())

        tr = config.trend()
        self.alter("config.py","business_id='%s'" %tr.business_id ,"business_id='%s'"%self.Bid_textbox.text())

        lm = config.len_limit()
        self.alter("config.py","limit=%s" %lm.limit ,"limit=%s"%self.lid_textbox.text())



        python = sys.executable
        file_name = sys.argv[0]

        os.execl(python, python, file_name)

    def alter(self,file,old_str,new_str):
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str,new_str)
                file_data += line
        with open(file,"w",encoding="utf-8") as f:
            f.write(file_data)







if __name__ == '__main__':
    #os.system("python server.py")
    #os.system("python application.py")
    app = QApplication(sys.argv)
    ex = DB_min()
    sys.exit(app.exec_()) 

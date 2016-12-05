# -*- coding: utf-8 -*-
__author__ = 'xiazhou'
import sys
import os
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox,QLineEdit,QInputDialog,QFileDialog
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import *  
from untitled import *
import requests
import urllib


class download(QThread):
    trigger = pyqtSignal()
    trigger_2 = pyqtSignal([str])
    def __init__(self,id,directory):
        super(download,self).__init__()
        self.url = 'http://music.163.com/api/playlist/detail?id='+str(id)
        self.dir = directory
    def run(self):
        self.count = 0
        global is_downing
        self.r = requests.get(self.url)
        self.arr = self.r.json()['result']['tracks']
        for i in range(0,1000):
            try:
                name = self.arr[i]['name'] + '.mp3'
                self.trigger_2.emit(name)
                link = self.arr[i]['mp3Url']
                urllib.request.urlretrieve(link,self.dir + '\\'+name)	# 提前要在同一目录下创建 网易云音乐 文件夹
                self.count = 0
            except:
                self.count += 1
                if self.count == 10:
                    break
        self.trigger.emit()    
        
class mywindow(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button1_down)
        self.pushButton_2.clicked.connect(self.button2_down)
        self.is_downing = False
        self.directory = os.getcwd()
        self.textEdit_3.setText(os.getcwd())
        
    def button1_down(self):
        self.url = self.textEdit.toPlainText()
        self.id = self.url.split('=')[-1]
        if (self.id == '' or self.url.split('=')[-1] == self.url.split('=')[0]):
            self.textEdit_2.append('无效网址')
        else:
            if (self.is_downing == True):
                self.textEdit_2.append('下载尚未完成')
            else:
                self.downloader = download(self.id,self.directory)
                self.downloader.trigger.connect(threadend)
                self.downloader.trigger_2.connect(threadrun)
                self.downloader.start()
                self.textEdit_2.append('开始下载')
                self.is_downing = True
    def button2_down(self):
        self.directory = QFileDialog.getExistingDirectory(self,  
                                    "选取文件夹",  
                                    self.directory)
        self.textEdit_3.setText(self.directory)
        
def threadend():
    myshow.is_downing = False
    myshow.textEdit_2.append('下载已完成')
        
def threadrun(name):
    myshow.textEdit_2.append('正在下载：' + name)
 
app=QtWidgets.QApplication(sys.argv)
myshow=mywindow()  
myshow.show()

sys.exit(app.exec_()) 
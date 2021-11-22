import sqlite3

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from classes import GetSettings


GEVENT_SUPPORT=True


class UiLang():
    def __init__(self, obj):
        self.obj = obj

    def changeText(self, orig):
        data = sqlite3.connect("files/data.db")
        cur = data.cursor()
        if GetSettings.Lang() == 'Russian':
            result = cur.execute("""SELECT Russian FROM lang 
                                    WHERE English = ?""", (orig, )).fetchall()
            data.close()
        elif GetSettings.Lang() == 'English':
            result = cur.execute("""SELECT English FROM lang 
                                    WHERE English = ?""", (orig, )).fetchall()
        return result[0][0]

    def translateMain(self):
        self.obj.nick.setText(self.changeText('Nickname'))
        self.obj.search.setText(self.changeText('Search'))
        self.obj.rem.setText(self.changeText('remember'))
        self.obj.download.setText(self.changeText('Download skin'))
        self.obj.setShow.setText(self.changeText('Settings'))
        self.obj.tabWidget.setTabText(0, self.changeText('Mojang info'))
        self.obj.tabWidget.setTabText(1, self.changeText('Hypixel info'))
        self.obj.tabWidget_2.setTabText(0, self.changeText('Player'))
        self.obj.tabWidget_2.setTabText(1, self.changeText('SkyWars'))

    def translateErs(self, text):
        return self.changeText(text)

    def translateSettings(self):
        self.obj.setWindowTitle(self.changeText('Settings'))
        self.obj.hypeKey.setText(self.changeText('Hypixel API key'))
        self.obj.lang.setText(self.changeText('Language'))
        self.obj.defNick.setText(self.changeText('Default Search'))
        self.obj.saveApi.setText(self.changeText('Save'))
        self.obj.saveLang.setText(self.changeText('Save'))
        self.obj.saveNick.setText(self.changeText('Save'))
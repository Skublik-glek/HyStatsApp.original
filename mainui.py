import webbrowser, sys

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from classes import Mojang, Hypixel_main, GetSettings, SetSettings, CheckSettings, Hypixel_sw
from lang import UiLang


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('uis/main.ui', self)
        self.download.hide()

        self.KEY_API = GetSettings.HypixelAPI()
        self.flag = 0


        self.search.clicked.connect(self.newSearchMojang)

        self.download.clicked.connect(lambda: webbrowser.open(f'https://crafatar.com/skins/{self.uuid}'))

        self.search.clicked.connect(self.searchHypixelMain)
        self.search.clicked.connect(self.selectFirst)
        self.tabWidget_2.currentChanged.connect(self.tabSignal)
        self.setShow.clicked.connect(self.showSettings)
        self.search.clicked.connect(self.remember)

        self.nickInput.setText(GetSettings.Nick())
        

    def newSearchMojang(self):
        try:
            self.oldNicks.clear()

            self.searchMojang = Mojang(self.nickInput.text())
        
            self.uuid = self.searchMojang.uuid
            self.idBar.setText(self.uuid)

            for nick in self.searchMojang.old_names():
                snick = nick["name"]
                self.oldNicks.addItem(snick)

            self.orig_nick = self.searchMojang.correct_name()
            self.nickInput.setText(self.orig_nick)

            skin = self.searchMojang.skin()
            self.skinmap = QPixmap()
            self.skinmap.loadFromData(skin)
            self.skinView.setPixmap(self.skinmap)
            self.download.show()
        except Exception:
            translate = UiLang(self)
            self.nickInput.setText(translate.translateErs("Invalid Player"))
            self.uuid = ""
            self.idBar.clear()
            self.skinView.clear()
            self.download.hide()

    def searchHypixelMain(self):
        try:
            self.hypixel = Hypixel_main(self.KEY_API, self.uuid)
            text = f"Level: {int(self.hypixel.lvl())}\nKarma: {self.hypixel.karma()}\
                    \nAchievement points: {self.hypixel.achievement_points()}"
            self.mainInfo.setFont(QFont('Arial', 18))
            self.mainInfo.setText(text)
            self.rank.setHtml(f"<font size = 18 >Rank:</font> {self.hypixel.rank()}")
            self.guild.setHtml(self.hypixel.guildname())
            self.login.setText(self.hypixel.get_session())
        except Exception:
            self.mainInfo.clear()
            self.rank.clear()
            self.guild.clear()
            self.login.clear()

    def searchHypixelSw(self):
        try:
            self.hypixelSw = Hypixel_sw(self.KEY_API, self.uuid)
            textSw = f"""Level: {self.hypixelSw.getLevel()}
Kills: {self.hypixelSw.getKills()}
Deaths: {self.hypixelSw.getDeaths()}
Wins: {self.hypixelSw.getWins()}
Looses: {self.hypixelSw.getLooses()}
K/D: {self.hypixelSw.getKd()}
W/L: {self.hypixelSw.getWl()}"""
            textRunkedSw = f"""Kills: {self.hypixelSw.getRankedKills()}
Deaths: {self.hypixelSw.getRankedDeaths()}
Wins: {self.hypixelSw.getRankedWins()}
Looses: {self.hypixelSw.getRankedLooses()}
K/D: {self.hypixelSw.getRankedKd()}
W/L: {self.hypixelSw.getRankedWl()}"""
            self.swStats.setFont(QFont('Arial', 14))
            self.rSwStats.setFont(QFont('Arial', 14))
            self.swStats.setText(textSw)
            self.rSwStats.setText(textRunkedSw)
        except:
            self.swStats.clear()
            self.rSwStats.clear()

    def remember(self):
        if self.rem.isChecked() == True and self.nickInput.text() not in ["Несуществующий Игрок", "Invalid Player"]:
            SetSettings.setDefaultNick(self.nickInput.text())

    def tabSignal(self):
        if self.sender().currentIndex() == 1 and self.flag != 1:
            self.searchHypixelSw()
        self.flag = 1

    def showSettings(self):
        self.set = Settings()
        translate = UiLang(self.set)
        translate.translateSettings()
        self.set.show()

    def selectFirst(self):
        self.tabWidget_2.setCurrentIndex(0)
        self.flag = 0


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)

        uic.loadUi('uis/settings.ui', self)
        
        self.saveApi.clicked.connect(self.setApi)
        self.saveNick.clicked.connect(self.setNick)
        self.saveLang.clicked.connect(self.setLang)

        self.apiEdit.setText(GetSettings.HypixelAPI())
        self.nickEdit.setText(GetSettings.Nick())

    def setApi(self):
        check = CheckSettings()
        if check.keyValid(self.apiEdit.text()):
            SetSettings.setHypixelApi(self.apiEdit.text())
        else:
            translate = UiLang(self)
            self.apiEdit.setText(translate.translateErs("Invalid Api"))

    def setNick(self):
        SetSettings.setDefaultNick(self.nickEdit.text())

    def setLang(self):
        SetSettings.setLang(self.langEdit.currentText())
        sys.exit()
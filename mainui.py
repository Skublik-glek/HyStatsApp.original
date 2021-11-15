import webbrowser

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from classes import Mojang, Hypixel_main, GetSettings, SetSettings, CheckSettings


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('uis/main.ui', self)
        self.download.hide()

        self.KEY_API = GetSettings.HypixelAPI()


        self.search.clicked.connect(self.newSearchMojang)

        self.download.clicked.connect(lambda: webbrowser.open(f'https://crafatar.com/skins/{self.uuid}'))

        self.search.clicked.connect(self.searchHypixelMain)
        self.search.clicked.connect(self.selectFirst)
        self.setShow.clicked.connect(self.showSettings)

        self.setStyleSheet("""background-color: rgba(251, 215, 252, 1);""")
        self.search.setStyleSheet("""background-color: green; 
                                     padding: 7px; border-radius: 10px; 
                                     border: 2px solid rgba(249, 135, 255, 1);""")
        self.nickInput.setStyleSheet("""padding: 5px; border-radius: 10px; 
                                     border: 2px solid rgba(249, 135, 255, 1);""")

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
            self.nickInput.setText("Invalid Player")
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

    def showSettings(self):
        self.set = Settings()
        self.set.show()

    def selectFirst(self):
        self.tabWidget_2.setCurrentIndex(0)


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
            self.apiEdit.setText("Invalid Api")

    def setNick(self):
        SetSettings.setDefaultNick(self.nickEdit.text())

    def setLang(self):
        SetSettings.setLang(self.langEdit.currentText())
        


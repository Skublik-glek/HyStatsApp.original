import sys

from PyQt5.QtWidgets import QApplication, QInputDialog

from mainui import Main
from classes import SetSettings, GetSettings, CheckSettings


KEY_API = GetSettings.HypixelAPI()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    sys.excepthook = except_hook
    ex.show()
    check = CheckSettings()
    while not check.keyCheck():
        KEY_API, ok = QInputDialog.getText(ex, 'Hypixel API',
            'Enter your Hypixel API key:')
        if ok:
            if check.keyValid(KEY_API):
                SetSettings.setHypixelApi(KEY_API)
        else:
            sys.exit()
    sys.exit(app.exec())
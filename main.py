import sys

from PyQt5.QtWidgets import QApplication, QInputDialog

from mainui import Main
from classes import SetSettings, GetSettings, CheckSettings
from lang import UiLang


KEY_API = GetSettings.HypixelAPI()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    styleSheet = """
QWidget {
    background-color: rgba(163, 158, 158, 1);
}

QLineEdit {
    padding: 5px; 
    border-radius: 10px; 
    border: 2px solid rgba(97, 97, 97, 1);
}

QPushButton {
    background-color: rgba(130, 125, 125, 1); 
    padding: 7px; border-radius: 10px; 
    border: 2px solid rgba(97, 97, 97, 1);
}

QTabBar::tab {
    background-color: rgba(130, 125, 125, 1);
    border: 2px solid rgba(97, 97, 97, 1);
    border-bottom-color: rgba(97, 97, 97, 1);
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    min-width: 16ex;
    padding: 2px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: #c6b8de;
}

QTabBar::tab:!selected {
    margin-top: 4px;
}
 
QTabWidget::pane { border: 4px solid rgba(97, 97, 97, 1); }
"""
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    ex = Main()
    translate = UiLang(ex)
    translate.translateMain()
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
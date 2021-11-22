import sys

from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5 import QtGui

from mainui import Main
from classes import SetSettings, GetSettings, CheckSettings
from lang import UiLang


KEY_API = GetSettings.HypixelAPI()
GEVENT_SUPPORT=True
# hi git

try:
    from PyQt5.QtWinExtras import QtWin                                        
    myappid = 'SkublikCorp.EasyApps.HyStatsApp.0.1.2'                          
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)                       
except ImportError:
    pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    styleSheet = """
QWidget {
    margin-left: 2px;
    margin-right: 2px;
    margin-top: 2px;
    margin-bottom: 2px;
    background-color: rgba(163, 158, 158, 1);
}

QLineEdit {
    background-color: rgba(194, 194, 194, 1);
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
    app.setWindowIcon(QtGui.QIcon('files/logo.png'))
    app.setStyleSheet(styleSheet)
    ex = Main()
    ex.setWindowIcon(QtGui.QIcon('files/logo.png'))
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
import zapret
import sys
import ctypes
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Qt

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(sys.argv),
        None,
        1
    )
    sys.exit(0)

if not is_admin():
    restart_as_admin()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Roblox Zapr")
        self.setFixedSize(300, 300)

        self.button = QPushButton("Start", self)
        self.button.setGeometry(100, 130, 100, 40)
        self.button.clicked.connect(self.start)

    def start(self):
        zapret.start()
        self.button.setText("Stop")
        self.button.clicked.disconnect()
        self.button.clicked.connect(self.stop)

    def stop(self):
        zapret.stop()
        self.button.setText("Start")
        self.button.clicked.disconnect()
        self.button.clicked.connect(self.start)

    def closeEvent(self, event):
        try:
            zapret.stop()
        except:
            pass
        event.accept()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

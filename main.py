import sys
import ctypes
import zapret
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QComboBox, QLabel, QMessageBox,
    QSystemTrayIcon, QMenu
)
from PySide6.QtCore import QTimer, Qt, QEvent
from PySide6.QtGui import QIcon

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

        self.setWindowTitle("Roblox Zapret")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Выбор конфигурации:"))

        self.combo = QComboBox()
        self.combo.addItems(list(zapret.CONFIGS.keys()))
        layout.addWidget(self.combo)

        self.button = QPushButton()
        self.button.clicked.connect(self.toggle)
        layout.addWidget(self.button)

        self.check_btn = QPushButton("Проверить")
        self.check_btn.clicked.connect(self.manual_check)
        layout.addWidget(self.check_btn)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_button_state)
        self.timer.start(2000)

        self.running = False
        self.update_button_state()

        self.init_tray()
    def init_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                self,
                "Ошибка",
                "Системный трей недоступен"
            )
            sys.exit(1)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icon.ico"))
        self.tray.setToolTip("Roblox Zapret")

        menu = QMenu()

        show_action = menu.addAction("Открыть")
        show_action.triggered.connect(self.show_window)

        exit_action = menu.addAction("Выход")
        exit_action.triggered.connect(self.exit_app)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.tray_click)
        self.tray.show()

    def tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()

    def show_window(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.raise_()
        self.activateWindow()

    def exit_app(self):
        if zapret.is_running():
            zapret.stop()
        QApplication.quit()

    def update_button_state(self):
        if zapret.is_running():
            self.button.setText("Stop")
            self.running = True
        else:
            self.button.setText("Start")
            self.running = False

    def toggle(self):
        if self.running:
            zapret.stop()
            self.update_button_state()
        else:
            config_name = self.combo.currentText()
            zapret.start(config_name)
            if zapret.is_running():
                self.update_button_state()
            else:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "winws.exe не удалось запустить"
                )
                self.update_button_state()

    def manual_check(self):
        if zapret.is_running():
            QMessageBox.information(self, "Проверка", "winws.exe запущен")
        else:
            QMessageBox.warning(self, "Проверка", "winws.exe не запущен")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.showMessage(
            "Roblox Zapret",
            "Приложение свернуто в трей",
            QSystemTrayIcon.Information,
            2000
        )

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMinimized():
                QTimer.singleShot(0, self.hide)
        super().changeEvent(event)
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
app.setWindowIcon(QIcon("icon.ico"))
window = MainWindow()
window.show()
sys.exit(app.exec())
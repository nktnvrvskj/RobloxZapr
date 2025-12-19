import sys
import ctypes
import zapret
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QLabel, QMessageBox
from PySide6.QtCore import QTimer

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

        # Таймер автопроверки каждые 2 секунды
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_button_state)
        self.timer.start(2000)

        self.update_button_state()

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
        if zapret.is_running():
            zapret.stop()
        event.accept()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

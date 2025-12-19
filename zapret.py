import os
import sys
import subprocess
import psutil
import ctypes
import logging
import importlib.util

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Определяем папку exe или скрипта
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Динамическая загрузка configs.py (НЕ компилируется)
CONFIGS_PATH = os.path.join(BASE_DIR, "configs.py")
if not os.path.exists(CONFIGS_PATH):
    raise FileNotFoundError(f"configs.py не найден рядом с {BASE_DIR}")

spec = importlib.util.spec_from_file_location("configs", CONFIGS_PATH)
configs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(configs)

CONFIGS = configs.CONFIGS
BIN_DIR = configs.BIN_DIR

WINWS_PATH = os.path.join(BIN_DIR, "winws.exe")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_running():
    for p in psutil.process_iter(['name']):
        if p.info['name'] == 'winws.exe':
            return True
    return False

def start(config_name: str):
    if config_name not in CONFIGS:
        logging.error("Конфигурация не найдена")
        return

    if is_running():
        logging.info("winws.exe уже запущен")
        return

    if not os.path.exists(WINWS_PATH):
        logging.error(f"winws.exe не найден: {WINWS_PATH}")
        return

    args = CONFIGS[config_name]
    logging.info(f"Запуск winws.exe без окна")

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    subprocess.Popen(
        [WINWS_PATH] + args,
        cwd=BIN_DIR,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    logging.info(f"winws.exe запущен с конфигурацией: {config_name}")


def stop():
    found = False
    for p in psutil.process_iter(['name']):
        if p.info['name'] == 'winws.exe':
            p.terminate()
            found = True

    if found:
        logging.info("winws.exe остановлен")
    else:
        logging.error("winws.exe не найден")

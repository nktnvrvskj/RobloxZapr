import subprocess
import psutil
import ctypes
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BIN_DIR = os.path.join(BASE_DIR, "bin")
WINWS_PATH = os.path.join(BIN_DIR, "winws.exe")

LIST_PATH = os.path.join(BASE_DIR, "lists", "list-ultimate.txt")
DISCORD_IPSET_PATH = os.path.join(BASE_DIR, "lists", "ipset-discord.txt")
CLOUDFLARE_IPSET_PATH = os.path.join(BASE_DIR,"lists", "ipset-cloudflare.txt")

QUIC_GOOGLE = os.path.join(BIN_DIR, "quic_initial_www_google_com.bin")
TLS_GOOGLE = os.path.join(BIN_DIR, "tls_clienthello_www_google_com.bin")

ARGS = [
    "--wf-tcp=80,4433",
    "--wf-udp=443,1400,596-599,50000-50100",

    "--filter-udp=443",
    f'--hostlist={LIST_PATH}',
    "--dpi-desync=fake",
    "--dpi-desync-repeats=6",
    f'--dpi-desync-fake-quic={QUIC_GOOGLE}',
    "--new",

    "--filter-udp=1400,596-599,50000-50100",
    f'--ipset={DISCORD_IPSET_PATH}',
    "--dpi-desync=fake",
    "--dpi-desync-any-protocol",
    "--dpi-desync-cutoff=d3",
    "--dpi-desync-repeats=6",
    "--new",

    "--filter-tcp=80",
    f'--hostlist={LIST_PATH}',
    "--dpi-desync=fake,split2",
    "--dpi-desync-autottl=2",
    "--dpi-desync-fooling=md5sig",
    "--new",

    "--filter-tcp=443",
    f'--hostlist={LIST_PATH}',
    "--dpi-desync=split2",
    "--dpi-desync-split-seqovl=652",
    "--dpi-desync-split-pos=2",
    f'--dpi-desync-split-seqovl-pattern={TLS_GOOGLE}',
    "--new",

    "--filter-udp=443",
    f'--ipset={CLOUDFLARE_IPSET_PATH}',
    "--dpi-desync=fake",
    "--dpi-desync-repeats=6",
    f'--dpi-desync-fake-quic={QUIC_GOOGLE}',
    "--new",

    "--filter-tcp=80",
    f'--ipset={CLOUDFLARE_IPSET_PATH}',
    "--dpi-desync=fake,split2",
    "--dpi-desync-autottl=2",
    "--dpi-desync-fooling=md5sig",
    "--new",

    "--filter-tcp=443",
    f'--ipset={CLOUDFLARE_IPSET_PATH}',
    "--dpi-desync=split2",
    "--dpi-desync-split-seqovl=652",
    "--dpi-desync-split-pos=2",
    f'--dpi-desync-split-seqovl-pattern={TLS_GOOGLE}',
]

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

def is_running():
    for p in psutil.process_iter(['name']):
        if p.info['name'] == 'winws.exe':
            return True
    return False

def start():
    if is_running():
        print("winws.exe уже запущен")
        return

    subprocess.Popen(
        [WINWS_PATH] + ARGS,
        cwd=BIN_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("winws.exe запущен")

def stop():
    found = False
    for p in psutil.process_iter(['name']):
        if p.info['name'] == 'winws.exe':
            p.terminate()
            found = True

    if found:
        print("winws.exe остановлен")
    else:
        print("winws.exe не найден")

if __name__ == "__main__":
    if not is_admin():
        restart_as_admin()

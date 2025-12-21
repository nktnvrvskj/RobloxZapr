import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BIN_DIR = os.path.join(BASE_DIR, "bin")
LIST_PATH = os.path.join(BASE_DIR, "lists", "list-ultimate.txt")
DISCORD_IPSET_PATH = os.path.join(BASE_DIR, "lists", "ipset-discord.txt")
CLOUDFLARE_IPSET_PATH = os.path.join(BASE_DIR, "lists", "ipset-cloudflare.txt")

QUIC_GOOGLE = os.path.join(BIN_DIR, "quic_initial_www_google_com.bin")
TLS_GOOGLE = os.path.join(BIN_DIR, "tls_clienthello_www_google_com.bin")

CONFIGS = {
    "Roblox": [
        "--wf-tcp=80,4433",
        "--wf-udp=443,1400,596-599,50000-50100",
        "--filter-udp=443",
        f"--hostlist={LIST_PATH}",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=6",
        f"--dpi-desync-fake-quic={QUIC_GOOGLE}",
        "--new",
        "--filter-udp=1400,596-599,50000-50100",
        f"--ipset={DISCORD_IPSET_PATH}",
        "--dpi-desync=fake",
        "--dpi-desync-any-protocol",
        "--dpi-desync-cutoff=d3",
        "--dpi-desync-repeats=6",
        "--new",
    ],
    "Cloudflare Only": [
        "--filter-udp=443",
        f"--hostlist={LIST_PATH}",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=6",
    ],
    "Minimal": [
        "--filter-tcp=80",
        f"--hostlist={LIST_PATH}",
        "--dpi-desync=fake",
    ],
}

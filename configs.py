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
        "--wf-tcp=80,443",
        "--dpi-desync-split-pos=method+2",
        "--dpi-desync=multisplit",
        "--wf-udp=443,1400,596-599,50000-50100",
        "--filter-udp=443",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=6",
        f"--dpi-desync-fake-quic={QUIC_GOOGLE}",
        "--new",
        "--filter-udp=1400,596-599,50000-50100",
        "--filter-l7=discord,stun",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=6",
        "--new",
        "--filter-tcp=80",
        "--dpi-desync=fake,multisplit",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=md5sig",
        "--new",
        "--filter-tcp=443",
        "--dpi-desync=multisplit",
        "--dpi-desync-split-seqovl=652",
        "--dpi-desync-split-pos=2",
        f"--dpi-desync-split-seqovl-pattern={TLS_GOOGLE}",
        "--new",
        "--filter-udp=443",
        "--dpi-desync=fake",
        "--dpi-desync-repeats=6",
        f"--dpi-desync-fake-quic={QUIC_GOOGLE}",
        "--new",
        "--filter-tcp=80",
        "--dpi-desync=fake,multisplit",
        "--dpi-desync-autottl=2",
        "--dpi-desync-fooling=md5sig",
        "--new",
        "--filter-tcp=443",
        "--dpi-desync=multisplit",
        "--dpi-desync-split-seqovl=652",
        "--dpi-desync-split-pos=2",
        f"--dpi-desync-split-seqovl-pattern={TLS_GOOGLE}",
        "--new",
        "--dpi-desync=fake",
        "--dpi-desync-autottl=2",
        "--dpi-desync-repeats=12",
        "--dpi-desync-any-protocol=1",
        f"--dpi-desync-fake-unknown-udp={QUIC_GOOGLE}",
        "--dpi-desync-cutoff=n2",
    ],
}

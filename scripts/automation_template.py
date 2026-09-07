#!/usr/bin/env python3
"""Template otomatisasi aman untuk proyek Sunflower Land.

Template ini hanya memeriksa ketersediaan halaman game dan menjalankan hook
lokal milik Anda. Ia tidak berinteraksi dengan UI game, wallet, akun Telegram,
atau blockchain. Gunakan API resmi bila suatu saat menambahkan integrasi.
"""

from __future__ import annotations

import argparse
import logging
import time
import urllib.error
import urllib.request

DEFAULT_GAME_URL = "https://sunflower-land.com/play/"

def check_game(url: str, timeout: float) -> bool:
    """Catat apakah halaman game dapat diakses tanpa mengubah state apa pun."""
    request = urllib.request.Request(url, headers={"User-Agent": "SunflowerTMA-Monitor/1.0"})
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            elapsed_ms = (time.perf_counter() - started) * 1000
            logging.info("Game reachable: HTTP %s in %.0f ms", response.status, elapsed_ms)
            return 200 <= response.status < 400
    except urllib.error.URLError as error:
        logging.warning("Game check failed: %s", error.reason)
        return False

def run_local_hook(game_is_online: bool) -> None:
    """Tambahkan otomatisasi lokal yang aman di sini, misalnya notifikasi.

    Jangan simpan seed phrase/private key dan jangan mengotomatiskan aksi game,
    klik UI, transaksi, atau klaim hadiah. Aksi tersebut harus dilakukan pemilik
    akun secara sadar melalui kanal/API resmi.
    """
    if not game_is_online:
        logging.info("Hook example: send a non-sensitive outage notification.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Safe Sunflower Land availability monitor")
    parser.add_argument("--url", default=DEFAULT_GAME_URL, help="URL status yang diperiksa")
    parser.add_argument("--interval", type=float, default=0, help="Detik antar pemeriksaan; 0 = sekali")
    parser.add_argument("--timeout", type=float, default=10, help="Batas waktu request dalam detik")
    args = parser.parse_args()
    if args.interval < 0 or args.timeout <= 0:
        parser.error("--interval harus >= 0 dan --timeout harus > 0")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    while True:
        run_local_hook(check_game(args.url, args.timeout))
        if args.interval == 0:
            return
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

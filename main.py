#!/usr/bin/env python3
"""
Sunflower Land - Telegram Mini App (TMA) Bot
Ditenagai oleh python-telegram-bot v20+ (Async IO) & Web3 Polygon Integration.
"""

import asyncio
import logging
import os
import sys
import time
from typing import Optional

import httpx
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Update,
    WebAppInfo,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# 1. Load Environment Variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "123456:abcdef")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://sunflower-tma.vercel.app")
SUNFLOWER_GAME_URL = os.getenv("SUNFLOWER_GAME_URL", "https://sunflower-land.com/play/")
SFL_CONTRACT_ADDRESS = "0xd1f9c58e33933a9970353798ac555049721a5948"

# 2. Setup Logging
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("SunflowerTMA")


# =====================================================================
# HELPER FUNCTIONS: PUBLIC API & SERVER CHECK
# =====================================================================

async def get_server_and_token_status() -> dict:
    """Mengambil status server Sunflower Land dan harga token $SFL dari CoinGecko secara async."""
    status_info = {
        "server_status": "Unknown",
        "latency_ms": 0,
        "sfl_usd": None,
        "sfl_idr": None,
        "change_24h": None,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }

    async with httpx.AsyncClient(timeout=6.0) as client:
        # A. Cek Server Ping Sunflower Land
        try:
            start_t = time.perf_counter()
            resp = await client.get("https://sunflower-land.com/play/", follow_redirects=True)
            latency = (time.perf_counter() - start_t) * 1000
            status_info["latency_ms"] = int(latency)
            if resp.status_code == 200:
                status_info["server_status"] = "🟢 Online (Normal)"
            else:
                status_info["server_status"] = f"🟡 HTTP {resp.status_code}"
        except Exception as e:
            logger.warning(f"Error checking Sunflower Land server: {e}")
            status_info["server_status"] = "🔴 Lambat / Tidak dapat dijangkau"

        # B. Cek Harga Token $SFL via CoinGecko
        try:
            cg_url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "sunflower-land",
                "vs_currencies": "usd,idr",
                "include_24hr_change": "true",
            }
            cg_resp = await client.get(cg_url, params=params)
            if cg_resp.status_code == 200:
                data = cg_resp.json().get("sunflower-land", {})
                status_info["sfl_usd"] = data.get("usd")
                status_info["sfl_idr"] = data.get("idr")
                status_info["change_24h"] = data.get("usd_24h_change")
        except Exception as e:
            logger.warning(f"Error checking CoinGecko: {e}")

    return status_info


def build_status_text(data: dict) -> str:
    """Format tampilan teks status server dan token."""
    usd = f"${data['sfl_usd']:.4f}" if data['sfl_usd'] is not None else "N/A"
    idr = f"Rp {int(data['sfl_idr']):,}".replace(",", ".") if data['sfl_idr'] is not None else "N/A"

    change_val = data['change_24h']
    if change_val is not None:
        sign = "+" if change_val >= 0 else ""
        icon = "📈" if change_val >= 0 else "📉"
        change_str = f"{icon} {sign}{change_val:.2f}%"
    else:
        change_str = "N/A"

    text = (
        "<b>📊 STATUS SUNFLOWER LAND & TOKEN $SFL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>🌐 Status Server:</b> {data['server_status']}\n"
        f"<b>⚡ Latensi:</b> {data['latency_ms']} ms\n"
        f"<b>🕒 Waktu Cek:</b> <code>{data['timestamp']}</code>\n\n"
        "<b>🪙 Tokenomics $SFL (Polygon PoS):</b>\n"
        f"• Harga USD: <b>{usd}</b>\n"
        f"• Harga IDR: <b>{idr}</b>\n"
        f"• Perubahan 24 Jam: <b>{change_str}</b>\n\n"
        "<b>📜 Smart Contract:</b>\n"
        f"<code>{SFL_CONTRACT_ADDRESS}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Gunakan tombol di bawah untuk membuka TMA atau memperbarui info.</i>"
    )
    return text


# =====================================================================
# COMMAND HANDLERS
# =====================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk perintah /start: Mengirim kartu sambutan dan tombol WebApp."""
    user = update.effective_user
    first_name = user.first_name if user else "Farmer"

    welcome_text = (
        f"🌻 <b>Selamat Datang di Sunflower Land TMA, {first_name}!</b> 🌻\n\n"
        "Bermain game metaverse Web3 terdesentralisasi <b>Sunflower Land</b> langsung di dalam obrolan Telegram secara <i>fullscreen</i>, cepat, dan interaktif!\n\n"
        "<b>✨ Fitur Unggulan TMA:</b>\n"
        "• 🎮 <b>Fullscreen Experience:</b> Tampilan penuh responsif tanpa border.\n"
        "• 🦊 <b>Web3 Wallet Ready:</b> Terhubung dengan MetaMask, OKX & Trust Wallet di jaringan Polygon.\n"
        "• 🌾 <b>Farming & Crafting:</b> Tanam bibit, panen hasil bumi, pelihara ternak, dan kembangkan pulau Anda.\n"
        "• 💰 <b>Live Token Tracker:</b> Pantau harga koin $SFL real-time.\n\n"
        "Klik tombol <b>'🌻 Buka Sunflower Land'</b> di bawah untuk mulai bermain sekarang!"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="🌻 Buka Sunflower Land (TMA)",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Cek Status Server & $SFL",
                callback_data="check_status",
            ),
            InlineKeyboardButton(
                text="❓ Panduan Bertani",
                callback_data="help_guide",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🌐 Situs Resmi",
                url="https://sunflower-land.com",
            ),
            InlineKeyboardButton(
                text="📈 DexScreener SFL",
                url=f"https://dexscreener.com/polygon/{SFL_CONTRACT_ADDRESS}",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )


async def farm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk perintah /farm atau /play: Peluncuran cepat ke dalam game."""
    farm_text = (
        "🌾 <b>Siap Mengelola Ladang Anda?</b>\n\n"
        "1. Klik tombol di bawah untuk membuka game secara instan.\n"
        "2. Pastikan wallet Anda berada di <b>Polygon Network</b>.\n"
        "3. Tanam biji bunga matahari, rawat pulau Anda, dan dapatkan $SFL!\n"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="🚜 Masuk Ladang Sekarang",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Cek Harga $SFL",
                callback_data="check_status",
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=farm_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk perintah /status: Menampilkan latensi dan harga token $SFL."""
    status_msg = await update.message.reply_text("⏳ <i>Memeriksa server dan mengambil data harga $SFL...</i>", parse_mode=ParseMode.HTML)
    data = await get_server_and_token_status()
    text = build_status_text(data)

    keyboard = [
        [
            InlineKeyboardButton(
                text="🌻 Buka Game",
                web_app=WebAppInfo(url=WEBAPP_URL),
            ),
            InlineKeyboardButton(
                text="🔄 Refresh Status",
                callback_data="refresh_status",
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await status_msg.edit_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk perintah /wallet: Petunjuk koneksi crypto wallet."""
    wallet_text = (
        "🦊 <b>PANDUAN WEB3 WALLET (POLYGON PoS)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Sunflower Land beroperasi di atas blockchain <b>Polygon PoS (Chain ID 137)</b>.\n\n"
        "<b>Cara Menghubungkan Wallet di TMA:</b>\n"
        "1. Buka Sunflower Land melalui tombol WebApp.\n"
        "2. Klik tombol <b>'Hubungkan Wallet'</b> di bilah atas.\n"
        "3. Pilih <b>MetaMask</b>, <b>OKX Wallet</b>, atau <b>Trust Wallet</b>.\n"
        "4. Konfirmasi permintaan koneksi akun Anda.\n\n"
        "<b>💡 Tips Gas Fee:</b>\n"
        "Siapkan sedikit token <b>POL (Polygon)</b> di wallet Anda (~0.1 - 0.5 POL sudah sangat cukup untuk ratusan transaksi panen & crafting).\n\n"
        f"<b>Contract Address Token $SFL:</b>\n"
        f"<code>{SFL_CONTRACT_ADDRESS}</code>"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="🌻 Buka Sunflower Land",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=wallet_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk perintah /help: Menampilkan daftar perintah dan bantuan."""
    help_text = (
        "📖 <b>PANDUAN BOT & TELEGRAM MINI APP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Berikut adalah daftar perintah yang tersedia:\n\n"
        "• /start - Membuka menu utama dan peluncur WebApp\n"
        "• /farm - Akses cepat masuk ke dalam game Sunflower Land\n"
        "• /status - Cek status server game dan harga real-time $SFL\n"
        "• /wallet - Panduan konfigurasi wallet Web3 (Polygon PoS)\n"
        "• /help - Menampilkan pesan panduan ini\n\n"
        "<b>Perlu Bantuan Lebih Lanjut?</b>\n"
        "Kunjungi dokumentasi resmi: <a href='https://docs.sunflower-land.com'>docs.sunflower-land.com</a>"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text="🌻 Mainkan Game Sekarang",
                web_app=WebAppInfo(url=WEBAPP_URL),
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text=help_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )


# =====================================================================
# CALLBACK QUERY HANDLER
# =====================================================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menangani aksi klik tombol inline (callback_data)."""
    query = update.callback_query
    await query.answer()

    if query.data in ("check_status", "refresh_status"):
        data = await get_server_and_token_status()
        text = build_status_text(data)
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🌻 Buka Game",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                ),
                InlineKeyboardButton(
                    text="🔄 Refresh Status",
                    callback_data="refresh_status",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="« Kembali ke Menu",
                    callback_data="back_to_menu",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.debug(f"Message not modified: {e}")

    elif query.data == "help_guide":
        guide_text = (
            "🌾 <b>PANDUAN DASAR SUNFLOWER LAND</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "1. <b>Tanam & Panen:</b> Beli biji Sunflower dari pedagang, tanam di tanah subur, tunggu matang, lalu panen.\n"
            "2. <b>Jual Hasil Panen:</b> Jual sayuran dan buah untuk mendapatkan koin $SFL.\n"
            "3. <b>Ekspansi Lahan:</b> Gunakan kayu, batu, dan besi untuk memperluas pulau Anda.\n"
            "4. <b>Crafting & NFT:</b> Buat item langka yang bisa diperdagangkan di marketplace Polygon."
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🌻 Buka Sunflower Land",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="« Kembali ke Menu",
                    callback_data="back_to_menu",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=guide_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )

    elif query.data == "back_to_menu":
        user = update.effective_user
        first_name = user.first_name if user else "Farmer"
        welcome_text = (
            f"🌻 <b>Sunflower Land TMA - Menu Utama</b>\n\n"
            f"Halo <b>{first_name}</b>, siap untuk kembali mengelola ladang metaverse Anda?"
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    text="🌻 Buka Sunflower Land (TMA)",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Cek Status Server & $SFL",
                    callback_data="check_status",
                ),
                InlineKeyboardButton(
                    text="❓ Panduan Bertani",
                    callback_data="help_guide",
                ),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )


# =====================================================================
# BOT STARTUP LIFECYCLE (POST INIT)
# =====================================================================

async def post_init(application: Application) -> None:
    """Inisialisasi set command dan tombol menu webapp bot."""
    bot = application.bot
    me = await bot.get_me()
    logger.info(f"Bot berhasil terhubung: @{me.username} (ID: {me.id})")

    # A. Daftarkan perintah bot agar muncul di menu obrolan Telegram
    commands = [
        ("start", "Membuka menu utama Sunflower Land TMA"),
        ("farm", "Akses langsung game Sunflower Land"),
        ("status", "Cek status server dan harga token $SFL"),
        ("wallet", "Panduan integrasi Web3 Wallet Polygon"),
        ("help", "Panduan dan bantuan penggunaan"),
    ]
    try:
        await bot.set_my_commands(commands)
        logger.info("Bot commands berhasil didaftarkan ke Telegram.")
    except Exception as e:
        logger.warning(f"Gagal mengatur my_commands: {e}")

    # B. Daftarkan Menu Button jika URL WebApp menggunakan HTTPS
    if WEBAPP_URL.startswith("https://"):
        try:
            menu_btn = MenuButtonWebApp(text="🌻 Play SFL", web_app=WebAppInfo(url=WEBAPP_URL))
            await bot.set_chat_menu_button(menu_button=menu_btn)
            logger.info(f"Chat Menu Button WebApp berhasil diaktifkan dengan URL: {WEBAPP_URL}")
        except Exception as e:
            logger.warning(f"Gagal mengatur Chat Menu Button: {e}")


# =====================================================================
# MAIN APPLICATION RUNNER
# =====================================================================

def main() -> None:
    """Fungsi utama untuk menjalankan Telegram Bot."""
    if not BOT_TOKEN or BOT_TOKEN in {"YOUR_BOT_TOKEN_HERE", "123456:abcdef"}:
        logger.error("TELEGRAM_BOT_TOKEN belum disetel! Harap isi di file .env")
        sys.exit(1)

    logger.info("Memulai Sunflower Land Telegram Mini App Bot...")
    logger.info(f"Target WebApp URL: {WEBAPP_URL}")

    # Inisialisasi ApplicationBuilder
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Daftarkan Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("farm", farm_command))
    application.add_handler(CommandHandler("play", farm_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("wallet", wallet_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(callback_handler))

    # Jalankan polling bot
    logger.info("Bot siap menerima pesan. Menjalankan polling...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

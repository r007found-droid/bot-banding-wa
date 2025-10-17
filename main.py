import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

# ──────────────
# STATE
NUM, DATE, REASON = range(3)

# ──────────────
# COMMAND START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya bot pembuat banding WhatsApp.\nKetik /banding untuk mulai.")

# ──────────────
# MULAI BANDUNG
async def banding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Masukkan nomor WhatsApp Anda (contoh: +62812xxxx):")
    return NUM

async def get_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["number"] = update.message.text
    await update.message.reply_text("Tanggal kena banned (contoh: 2025-10-15):")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("Alasan kena banned (contoh: kesalahan sistem, tidak spam, dll):")
    return REASON

async def get_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reason"] = update.message.text

    text = (
        f"📋 *Pesan Banding WhatsApp*\n\n"
        f"Nomor: {context.user_data['number']}\n"
        f"Tanggal: {context.user_data['date']}\n"
        f"Alasan: {context.user_data['reason']}\n\n"
        "Pesan:\n"
        "Halo Tim WhatsApp, saya percaya akun saya diblokir karena kesalahan. "
        "Mohon tinjau ulang akun saya. Terima kasih."
    )

    await update.message.reply_text(text, parse_mode="Markdown")
    await update.message.reply_text(
        "📌 Langkah selanjutnya:\n"
        "1️⃣ Buka WhatsApp Anda.\n"
        "2️⃣ Tekan *Request a Review* saat muncul notifikasi banned.\n"
        "3️⃣ Salin pesan di atas ke kolom banding."
    )
    return ConversationHandler.END

# ──────────────
# CANCEL
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dibatalkan. Ketik /banding untuk mulai lagi.")
    return ConversationHandler.END

# ──────────────
# MAIN FUNCTION
def main():
    token = os.getenv("BOT_TOKEN")  # ambil token dari Railway Variable
    if not token:
        print("❌ ERROR: BOT_TOKEN belum diset di Railway Variables.")
        return

    app = ApplicationBuilder().token(token).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("banding", banding)],
        states={
            NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_num)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    print("✅ Bot sedang berjalan di Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()

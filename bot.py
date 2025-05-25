from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
#TOKEN = os.environ["BOT_TOKEN"]
TOKEN = "7990873992:AAH4aQzGa7Lm5QKe6oWMYlEt1LDmnghc_sc"

# Dizionario di traduzioni
LANG_MESSAGES = {
    "it": "Come posso esserti utile?",
    "en": "How can I help you?",
    "es": "¿Cómo puedo ayudarte?",
    "pt": "Como posso te ajudar?"
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇮🇹 Italiano", callback_data="lang_it"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ],
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = (
        "Ciao! 👋 Sono ForTu, il Bot che ti accompagnerà nelle giornate di accoglienza "
        "nella diocesi di Orvieto-Todi.\nIn che lingua vuoi parlarmi? 🌍"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Gestione della lingua scelta
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.replace("lang_", "")
    response = LANG_MESSAGES.get(lang, "How can I help you?")
    await query.edit_message_text(text=response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language, pattern="^lang_"))

    print("✅ Bot multilingua avviato.")
    app.run_polling()


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

#TOKEN = os.environ["BOT_TOKEN"]
TOKEN = "8015077440:AAHaL2yfBbranjcoySyDx7f5Fw5TjWFhDbY"

# Traduzioni dei testi
LANG_TEXTS = {
    "it": {
        "greeting": "Come posso esserti utile?",
        "buttons": [
            ("📍 Dov'è la segreteria", "office"),
            ("🚻 Dove sono i bagni", "bathroom"),
            ("ℹ️ Dov'è il centro informazioni", "info"),
        ],
    },
    "en": {
        "greeting": "How can I help you?",
        "buttons": [
            ("📍 Where is the office?", "office"),
            ("🚻 Where are the bathrooms?", "bathroom"),
            ("ℹ️ Where is the info point?", "info"),
        ],
    },
    "es": {
        "greeting": "¿Cómo puedo ayudarte?",
        "buttons": [
            ("📍 ¿Dónde está la secretaría?", "office"),
            ("🚻 ¿Dónde están los baños?", "bathroom"),
            ("ℹ️ ¿Dónde está el punto de información?", "info"),
        ],
    },
    "pt": {
        "greeting": "Como posso te ajudar?",
        "buttons": [
            ("📍 Onde fica a secretaria?", "office"),
            ("🚻 Onde ficam os banheiros?", "bathroom"),
            ("ℹ️ Onde fica o ponto de informações?", "info"),
        ],
    }
}

# Messaggio iniziale con scelta lingua
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
    welcome = (
        "Ciao! 👋 Sono ForTu, il Bot che ti accompagnerà nelle giornate di accoglienza "
        "nella diocesi di Orvieto-Todi.\nIn che lingua vuoi parlarmi? 🌍"
    )
    await update.message.reply_text(welcome, reply_markup=reply_markup)

# Dopo scelta lingua → invia messaggio + pulsanti
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.replace("lang_", "")
    context.user_data["lang"] = lang

    data = LANG_TEXTS.get(lang, LANG_TEXTS["en"])
    greeting = data["greeting"]
    buttons = data["buttons"]

    keyboard = [[InlineKeyboardButton(text, callback_data=f"req_{code}")] for text, code in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(greeting)
    await query.message.reply_text("👇", reply_markup=reply_markup)

# Risposte ai pulsanti informativi
async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    code = query.data.replace("req_", "")
    lang = context.user_data.get("lang", "en")

    RESPONSES = {
        "office": {
            "it": "📍 La segreteria si trova presso l’edificio A, piano terra.",
            "en": "📍 The office is in Building A, ground floor.",
            "es": "📍 La secretaría está en el Edificio A, planta baja.",
            "pt": "📍 A secretaria fica no prédio A, térreo.",
        },
        "bathroom": {
            "it": "🚻 I bagni si trovano accanto alla mensa.",
            "en": "🚻 The bathrooms are next to the cafeteria.",
            "es": "🚻 Los baños están al lado del comedor.",
            "pt": "🚻 Os banheiros ficam ao lado do refeitório.",
        },
        "info": {
            "it": "ℹ️ Il centro informazioni è nella hall principale.",
            "en": "ℹ️ The info point is in the main hall.",
            "es": "ℹ️ El punto de información está en el vestíbulo principal.",
            "pt": "ℹ️ O ponto de informações fica no saguão principal.",
        }
    }

    msg = RESPONSES.get(code, {}).get(lang, "❓")
    await query.edit_message_text(msg)

    if code == "office":
        confirm_button = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🗺️ Vuoi aprire la mappa?", callback_data="show_map_yes"),
                InlineKeyboardButton("🔙 No, torna al menu", callback_data=f"lang_{lang}")
            ]
        ])
        await query.message.reply_text("Vuoi visualizzare la posizione sulla mappa?", reply_markup=confirm_button)

    elif code in ["bathroom", "info"]:
        back_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Torna al menu", callback_data=f"lang_{lang}")]
        ])
        await query.message.reply_text("", reply_markup=back_button)

# Gestione della scelta di aprire la mappa
async def handle_map_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")

    if query.data == "show_map_yes":
        latitude = 42.7161
        longitude = 12.0128
        maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        maps_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("🗺️ Apri in Google Maps", url=maps_url)],
            [InlineKeyboardButton("🔙 Torna al menu", callback_data=f"lang_{lang}")]
        ])
        await query.message.reply_location(latitude=latitude, longitude=longitude)
        await query.message.reply_text("Ecco la posizione su Google Maps:", reply_markup=maps_button)

# Setup bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_request, pattern="^req_"))
    app.add_handler(CallbackQueryHandler(handle_map_decision, pattern="^show_map_yes$"))

    print("✅ Bot multilingua con pulsanti avviato.")
    app.run_polling()


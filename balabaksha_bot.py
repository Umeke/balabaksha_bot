from telegram.ext import Updater, CommandHandler

# Сіздің боттың токені
TOKEN = '7669679530:AAELvjx9nGdCGvmarLibuhcpuw4zrxVyBkM'

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# Мысал деректер
menu = {
    'Топтар': ["Sabi stars тобы 3 жас, ортаңғы топ",
"Batyr baby тобы 3 жас, ортаңғы топ",
"Smart qadam тобы 4 жас, ересек топ",
"Leader bala тобы 5 жас, ересек топ",
"Qyran land тобы 5-6 жас, мектепалды даярлық топ"],
    'Жұмыс уақыты': {
       'Жұмыс уақыты': "Дүйсенбі - Жұма аралығында 08:00-18:30. Сенбі, Жексенбі демалыс."
    },
    'Төлемақы мөлшері': {
       "Төлемақы мөлшері" :" 65 000 теңгені құрайды",
    },
    'Үйірмелерімізді қарау': ["1. Хореография",
"2. Музыка",
"3. Интеллектум және логика ойындары",
"4. Логопед",
"5. Құм (арт) терапиясы",
"6. Тхэквондо"],
    'Балабақшаға келу үшін қандай құжаттар қажет?':["1. Бала денсаулығы паспорты",
"2. Эпидокружение анықтамасы",
"3. Туу туралы куәліктің көшірмесі",
"4. Ата-анасының жеке куәлігінің көшірмесі",
"5. 3 х 4 фото",
"6. 10 беттік көк папка"],
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Меню кнопкаларын құру
    keyboard = [
        ['Топтарды қарау', 'Жұмыс уақыты'],
        ['Төлемақы мөлшері', 'Үйірмелерімізді қарау'],
        ['Балабақшаға келу үшін қандай құжаттар қажет?']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Сәлеметсіз бе! Біздің балабақшаға қош келдіңіз!",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'Топтарды қарау':
        groups = '\n'.join(menu['Топтар'])
        await update.message.reply_text(f"Біздің топтар:\n{groups}")
    elif text == 'Жұмыс уақыты':
        schedules = '\n'.join([f"{group}: {time}" for group, time in menu['Жұмыс уақыты'].items()])
        await update.message.reply_text(f"Жұмыс уақыты:\n{schedules}")
    elif text == 'Төлемақы мөлшері':
        prices = '\n'.join([f"{group}: {price}" for group, price in menu['Төлемақы мөлшері'].items()])
        await update.message.reply_text(f"Төлемақы мөлшері:\n{prices}")
    elif text == 'Үйірмелерімізді қарау':
        activities = '\n'.join(menu['Үйірмелерімізді қарау'])
        await update.message.reply_text(f"Үйірмелерімізді қарау:\n{activities}")
    elif text == 'Балабақшаға келу үшін қандай құжаттар қажет?':
        activities = '\n'.join(menu['Балабақшаға келу үшін қандай құжаттар қажет?'])
        await update.message.reply_text(f"Балабақшаға келу үшін қандай құжаттар қажет?:\n{activities}")
    else:
        await update.message.reply_text("Кешіріңіз, сұрағыңызды түсінбедім.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))  # /help командасы да /start сияқты әрекет етеді

    # Барлық мәтіндік хабарларды өңдеу
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    main()
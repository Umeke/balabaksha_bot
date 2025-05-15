from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from telegram.request import HTTPXRequest
import logging

# Боттың токені
#TOKEN = '8019156726:AAFgg6yjrmZX8FtD-732cRSVJbi4sqxpqQI'

# HTTPXRequest арқылы таймаут параметрлерін орнату
request = HTTPXRequest(connect_timeout=60, read_timeout=60)

# Ботты жасау
app = ApplicationBuilder().token(TOKEN).request(request).build()

# Файлдар
work_schedule = {
    "3 жас ортаңғы “Sabi stars”": "sabi_time.pdf",
    "4 жас ересек “Batyr baby”": "batyr_time.pdf",
    "4 жас ересек “Smart qadam”": "smart_time.pdf",
    "5 жас мектепалды “Leader bala”": "leader_time.pdf",
    "5 жас мектепалды “Qyran land”": "qyran_time.pdf"
}

work_schedule1 = {
    "3 жас ортаңғы “Sabi stars”": "sabi_act.pdf",
    "4 жас ересек “Batyr baby”": "batyr_act.pdf",
    "4 жас ересек “Smart qadam”": "smart_act.pdf",
    "5 жас мектепалды “Leader bala”": "leader_act.pdf",
    "5 жас мектепалды “Qyran land”": "qyran_act.pdf"
}

text1 = {
    "Баланың балабақшаға бейімделуіне ата-ананың көмегі": [
        "1. Үйдегі жағдайды балаңыз келетін топтың күн режимімен сәйкестендіріңіз.",
        "2. Тәрбиешілерге бала туралы толық мәлімет беріңіз.",
        "3. Баланың өзіне-өзі қызмет ету қабілетін дамытыңыз.",
        "4. Балабақшаның тамақтану мәзірімен танысыңыз.",
        "5. Баланы махаббат пен қамқорлыққа бөлеңіз."
    ],
    "Баланың балабақшаға қиын бейімделу себептері": [
        "1. Басқа адамдармен қарым-қатынасқа түспеген.",
        "2. Өздігінен дәретке отырып үйренбеген.",
        "3. Балабақшада ұзақ уақыт болудан қорқу."
    ],
    "Ертеңгілік қоштасуды жеңілдету тәсілдері": [
        "1. Баламен тез қоштасыңыз.",
        "2. Балабақшаға келу рәсімін бірдей жасаңыз.",
        "3. Баланың сенімін нығайтыңыз."
    ],
    # SMART QADAM үшін кеңес орнына, батырм    а арқылы файл жүктеу шақырылады
    "SMART QADAM": "download_smart_qadam",
    "Leadar bala": "download_leader_bala",
}

# Мәзір
menu = {
    'Топтар': [
        "3 жас ортаңғы “Sabi stars”",
        "4 жас  ересек “Batyr baby”",
        "4 жас ересек “Smart qadam”",
        "5 жас  мектепалды “Leader bala”",
        "5 жас мектепалды ”Qyran land”"
    ],
    'Күн тәртібі': list(work_schedule.keys()),
    'Ұйымдастырылған іс-әрекет кестесі': list(work_schedule1.keys()),
    'Төлемақы мөлшері': [
        "Төлемақы мөлшері 95 000 теңгені құрайды",
    ],
    'Үйірмелерімізді қарау': [
        "1. Хореография",
        "2. Музыка",
        "3. Интеллектум және логика ойындары",
        "4. Логопед",
        "5. Құм (арт) терапиясы",
        "6. Тхэквондо",
        "7. Логопед",
        "Әр үйірме аптасына 2  рет өткізіледі"
    ],
    'Балабақшаға келу үшін қандай құжаттар қажет?': [
        "1. Бала денсаулығы паспорты",
        "2. Эпидокружение анықтамасы",
        "3. Туу туралы куәліктің көшірмесі",
        "4. Ата-анасының жеке куәлігінің көшірмесі",
        "5. 3 х 4 фото",
        "6. 10 беттік көк папка"
    ],
    'Балабақша мұрағаты': [
        "2017 ж.бастап өз жұмысын бастаған",
        "2022 ж. “Тәрбие тірегі” оқу-әдістемелік орталығы ұйымдастырған байқауда “Үздік балабақша” атағы.",
        "2024 ж. Мемлекеттік аттестатциядан өтті."
    ],
    'Ата-аналарға консультациялық кеңестер': list(text1.keys())
}

# Логгерді баптау
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# START командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['Топтар', 'Күн тәртібі'],
        ['Төлемақы мөлшері', 'Үйірмелерімізді қарау'],
        ['Балабақшаға келу үшін қандай құжаттар қажет?', 'Ата-аналарға консультациялық кеңестер'],
        ['Балабақша мұрағаты', 'Ұйымдастырылған іс-әрекет кестесі']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Сәлеметсіз бе! “Happy Kids” балабақшасына қош келдіңіз!",
        reply_markup=reply_markup
    )


# Мәтіндік хабарларды өңдеу
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'Күн тәртібі':
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"time_{index}")]
            for index, name in enumerate(menu['Күн тәртібі'])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Топтарды таңдаңыз:", reply_markup=reply_markup)
    elif text == 'Ұйымдастырылған іс-әрекет кестесі':
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"activity_{index}")]
            for index, name in enumerate(menu['Ұйымдастырылған іс-әрекет кестесі'])
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Іс-әрекетті таңдаңыз:", reply_markup=reply_markup)
    elif text == 'Ата-аналарға консультациялық кеңестер':
        keyboard = [
            [InlineKeyboardButton(topic, callback_data=f"advice_{index}")]
            for index, topic in enumerate(text1.keys())
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Тақырыпты таңдаңыз:", reply_markup=reply_markup)
    elif text in menu:
        activities = '\n'.join(menu[text]) if isinstance(menu[text], list) else str(menu[text])
        await update.message.reply_text(activities)
    else:
        await update.message.reply_text("Кешіріңіз, сұрағыңызды түсінбедім.")


# Батырмалар мен callback мәліметтерін өңдеу
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # SMART QADAM үшін файлды жүктеу батырмасы басылған жағдайда
    if query.data == "download_smart_qadam":
        file_path = "4 jas tasks.pdf"  # SMART QADAM файлының жолы
        try:
            with open(file_path, 'rb') as file:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=file,
                    caption="SMART QADAM"
                )
        except Exception as e:
            await query.message.reply_text(f"Файлды жүктеу кезінде қате орын алды: {e}")
        return

    if query.data == "download_leader_bala":
        file_path = "5 jas tasks.pdf"  # SMART QADAM файлының жолы
        try:
            with open(file_path, 'rb') as file:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=file,
                    caption="Leadar_bala"
                )
        except Exception as e:
            await query.message.reply_text(f"Файлды жүктеу кезінде қате орын алды: {e}")
        return

    data = query.data.split("_")
    action = data[0]
    index = int(data[1])

    if action == "time":
        group_name = menu['Күн тәртібі'][index]
        file_path = work_schedule[group_name]
        await send_file(query, context, file_path, group_name)
    elif action == "activity":
        group_name = menu['Ұйымдастырылған іс-әрекет кестесі'][index]
        file_path = work_schedule1[group_name]
        await send_file(query, context, file_path, group_name)
    elif action == "advice":
        topic = list(text1.keys())[index]
        # Егер таңдалған тақырып SMART QADAM болса, файлды жүктеу батырмасын көрсетеміз
        if topic == "SMART QADAM":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Файлды жүктеу", callback_data="download_smart_qadam")]
            ])
            await query.message.reply_text(
                "Төмендегі батырманы басып файлды жүктеңіз:",
                reply_markup=keyboard
            )
        elif topic == "Leadar bala":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Файлды жүктеу", callback_data="download_leader_bala")]
            ])
            await query.message.reply_text(
                "Төмендегі батырманы басып файлды жүктеңіз:",
                reply_markup=keyboard
            )
        else:
            advice = '\n'.join(text1[topic])
            await query.message.reply_text(advice)
    else:
        await query.message.reply_text("Белгісіз таңдау!")


# Файл жіберу функциясы
async def send_file(query, context, file_path, caption):
    try:
        with open(file_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file,
                caption=f"{caption}"
            )
    except Exception as e:
        await query.message.reply_text(f"Файлды жіберуде қате орын алды: {e}")


# Басты функция
def main():
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()


if __name__ == '__main__':
    main()

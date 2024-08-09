import logging
import os
import re
import pickle
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import datetime
import io
import pandas as pd
import dill
from sklearn.preprocessing import LabelEncoder

data_user = dict()
shapeList = list()
shapelist = [['bell'], ['conical'], ['convex'],
             ['flat'], ['sunken'], ['spherical'], ['others']]
shapedict = {'bell': 'b', 'conical': 'c', 'convex': 'x',
             'flat': 'f', 'sunken': 's', 'spherical': 'p', 'others': 'o'}
capcolorlist = [['brown'], ['buff'], ['gray'], ['green'], ['pink'],
                ['purple'], ['red'], ['white'], ['yellow'], ['blue'],
                ['orange'],  ['black']]
capcolordict = {'brown': 'n', 'buff': 'b', 'gray': 'g', 'green': 'r', 'pink': 'p', 'purple': 'u',
                'red': 'e', 'white': 'w', 'yellow': 'y', 'blue': 'l', 'orange': 'o',  'black': 'k'}
gillattachmentlist = [['adnate'], ['adnexed'], ['decurrent'], ['free'],
                      ['sinuate'], ['pores'], ['none']]
gillattachmentdict = {'adnate': 'a', 'adnexed': 'x', 'decurrent': 'd', 'free': 'e',
                      'sinuate': 's', 'pores': 'p', 'none': 'f'}
reply_keyboard_main = [["Check mushroom"]]
reply_keyboard_final = [["Verify if it's edible"]]
ringtypelist = [['cobwebby'], ['evanescent'], ['flaring'], ['grooved'], ['large'],
                ['pendant'], ['sheathing'], ['zone'], ['scaly'], ['movable'],
                ['none']]
ringtypedict = {'cobwebby': 'c', 'evanescent': 'e', 'flaring': 'r', 'grooved': 'g',
                'large': 'l', 'pendant': 'p', 'sheathing': 's', 'zone': 'z',
                'scaly': 'y', 'movable': 'm', 'none': 'f'}
hasringdict = {'yes': 1, 'no': 0}
habitatlist = [['grasses'], ['leaves'], ['meadows'], ['paths'], ['heaths'],
               ['urban'], ['waste'], ['woods']]
habitatdict = {'grasses': 'g', 'leaves': 'l', 'meadows': 'm', 'paths': 'p',
               'heaths': 'h', 'urban': 'u', 'waste': 'w', 'woods': 'd'}
seasonlist = [['spring'], ['summer'], ['autumn'], ['winter']]
seasondict = {'spring': 's', 'summer': 'u', 'autumn': 'a', 'winter': 'w'}
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
(
    ACTION,
    CAPSHAPE,
    CAPCOLOR,
    GILLATACHMENT,
    GILLCOLOR,
    STEMCOLOR,
    HASRING,
    RINGTYPE,
    CAPDIAMETR,
    STEMHEIGHT,
    STEMWIDTH,
    BRUISEBLEED,
    FINALACTION,
    HABITAT,
    SEASON,
    CANCEL
) = range(16)
# Старт бота


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Please, press 'check mushroom' to enter mushroom parameters",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_main, one_time_keyboard=True),
    )
    return ACTION

# действия при выборе пункта главного меню


async def get_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    logger.info(f"User {chat_id} get action: {update.message.text}")
    data_user.clear()
    reply_keyboard = shapelist
    await update.message.reply_text(
        "Choose cap shape",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )
    return CAPSHAPE


async def get_capshape(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in shapelist:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Choose cap color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['cap-shape'] = [shapedict[update.message.text]]

        return CAPCOLOR
    else:
        reply_keyboard = shapelist
        await update.message.reply_text(
            "Please, choose cap shape",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return CAPSHAPE


async def get_capcolor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in capcolorlist:
        reply_keyboard = gillattachmentlist
        await update.message.reply_text(
            "Choose gill atachment",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['cap-color'] = [capcolordict[update.message.text]]
        return GILLATACHMENT
    else:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Please, choose cap color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return CAPCOLOR


async def get_gillatachment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in gillattachmentlist:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Choose gill color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['gill-attachment'] = [gillattachmentdict[update.message.text]]
        return GILLCOLOR
    else:
        reply_keyboard = gillattachmentlist
        await update.message.reply_text(
            "Please, choose gill atachment",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return GILLATACHMENT


async def get_gillcolor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in capcolorlist:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Choose stem color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['gill-color'] = [capcolordict[update.message.text]]
        return STEMCOLOR
    else:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Please, choose gill color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return GILLCOLOR


async def get_stemcolor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in capcolorlist:
        reply_keyboard = [[]]
        reply_keyboard[0] = ['yes', 'no']
        await update.message.reply_text(
            "Has ring",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['stem-color'] = [capcolordict[update.message.text]]
        return HASRING
    else:
        reply_keyboard = capcolorlist
        await update.message.reply_text(
            "Please, choose stem color",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return STEMCOLOR


async def get_hasring(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif update.message.text == "yes" or update.message.text == "no":
        if hasringdict[update.message.text] == 1:
            reply_keyboard = ringtypelist
            await update.message.reply_text(
                "Choose ring type",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True),
            )
            data_user['has-ring'] = [hasringdict[update.message.text]]
            return RINGTYPE
        else:
            await update.message.reply_text(
                "Enter cap diameter (cm)",
                reply_markup=ReplyKeyboardRemove()
            )
            data_user['has-ring'] = [hasringdict[update.message.text]]
            data_user['ring-type'] = ['f']
            return CAPDIAMETR
    else:
        reply_keyboard = [[]]
        reply_keyboard[0] = ['yes', 'no']
        await update.message.reply_text(
            "Please choose an option for 'Has ring'",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return HASRING


async def get_ringtype(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in ringtypelist:
        await update.message.reply_text(
            "Enter cap diameter (cm)",
            reply_markup=ReplyKeyboardRemove()
        )
        data_user['ring-type'] = [ringtypedict[update.message.text]]
        return CAPDIAMETR
    else:
        reply_keyboard = ringtypelist
        await update.message.reply_text(
            "Choose ring type",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return RINGTYPE


async def get_capdiametr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif update.message.text.isdigit():
        await update.message.reply_text(
            "Enter stem height (cm)",
            reply_markup=ReplyKeyboardRemove()
        )
        data_user['cap-diameter'] = [update.message.text]
        return STEMHEIGHT
    else:
        await update.message.reply_text(
            "Incorrect input, please enter a number",
            reply_markup=ReplyKeyboardRemove()
        )
        return CAPDIAMETR


async def get_stemheight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif update.message.text.isdigit():
        await update.message.reply_text(
            "Enter stem width (mm)",
            reply_markup=ReplyKeyboardRemove(),
        )
        data_user['stem-height'] = [float(update.message.text)]
        return STEMWIDTH
    else:
        await update.message.reply_text(
            "Incorrect input, please enter a number",
            reply_markup=ReplyKeyboardRemove()
        )
        return STEMHEIGHT


async def get_stemwidth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif update.message.text.isdigit():
        reply_keyboard = [[]]
        reply_keyboard[0] = ['yes', 'no']
        await update.message.reply_text(
            "Does bruise/bleed",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['stem-width'] = [float(update.message.text)]
        return BRUISEBLEED
    else:
        await update.message.reply_text(
            "Incorrect input, please enter a number",
            reply_markup=ReplyKeyboardRemove()
        )
        return STEMWIDTH


async def get_bruisebleed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif update.message.text == "yes" or update.message.text == "no":
        reply_keyboard = habitatlist
        await update.message.reply_text(
            "Choose a habitat",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['does-bruise-or-bleed'] = [hasringdict[update.message.text]]
        return HABITAT
    else:
        reply_keyboard = [[]]
        reply_keyboard[0] = ['yes', 'no']
        await update.message.reply_text(
            "Please, choose an option for 'Does bruise/bleed'",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return BRUISEBLEED


async def get_habitat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in habitatlist:
        reply_keyboard = seasonlist
        await update.message.reply_text(
            "Choose a season",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        data_user['habitat'] = [habitatdict[update.message.text]]
        return SEASON
    else:
        reply_keyboard = habitatlist
        await update.message.reply_text(
            "Please, choose a habitat",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return HABITAT


async def get_season(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    elif [update.message.text] in seasonlist:
        await update.message.reply_text(
            "Let's verify this mushroom",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_final, one_time_keyboard=True),
        )
        data_user['season'] = [seasondict[update.message.text]]

        return FINALACTION
    else:
        reply_keyboard = seasonlist
        await update.message.reply_text(
            "Please, choose a season",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )
        return SEASON


async def get_finalaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "/start":
        await update.message.reply_text(
            "Please, press 'check mushroom' to enter mushroom parameters",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard_main),
        )
        return ACTION
    else:
        await update.message.reply_text(
            "Verifying if it's edible...",
            reply_markup=ReplyKeyboardRemove(),
        )
        # with open('model.pkl', 'rb') as file:
        #   model = pickle.load(file)
        with open("model.pkl", "rb") as dill_file:
            model = dill.load(dill_file)
        data_to_model = {'cap-diameter': data_user['cap-diameter'], 'cap-color': data_user['cap-color'], 'cap-shape': data_user['cap-shape'], 'does-bruise-or-bleed': data_user['does-bruise-or-bleed'], 'gill-attachment': data_user['gill-attachment'], 'gill-color': data_user['gill-color'],
                         'stem-height': data_user['stem-height'], 'stem-width': data_user['stem-width'], 'stem-color': data_user['stem-color'], 'has-ring': data_user['has-ring'], 'ring-type': data_user['ring-type'], 'habitat': data_user['habitat'], 'season': data_user['season']}
        X_NEW = pd.DataFrame(data_to_model)
        predicted_values = model.predict(X_NEW)
        if predicted_values[0] == 1:
            result = "it's poisonous"
        else:
            result = "it's edible"
        await update.message.reply_text(

            result,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_main, one_time_keyboard=True),
        )
        return ACTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.",      reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"{query.data}")

    # получает на вход диапазон ячеек, ключевое слово для поиска и номер столбца для возврата; возвращает массив значенийб удовлетворяющий критериям поиска


def main() -> None:
    application = (
        Application.builder()
        .token("6749284282:AAG-YqUF2Sa4rLVFU4YJltTew1RlF6VgMF4")
        .build()
    )
    application.add_handler(CallbackQueryHandler(button))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ACTION: [
                MessageHandler(None, get_action),
            ],
            CAPSHAPE: [
                MessageHandler(None, get_capshape),
            ],
            CAPCOLOR: [
                MessageHandler(None, get_capcolor),
            ],
            GILLATACHMENT: [
                MessageHandler(None, get_gillatachment),
            ],
            STEMCOLOR: [
                MessageHandler(None, get_stemcolor),
            ],
            GILLCOLOR: [
                MessageHandler(None, get_gillcolor),
            ],
            HASRING: [
                MessageHandler(None, get_hasring),
            ],
            RINGTYPE: [
                MessageHandler(None, get_ringtype),
            ],
            CAPDIAMETR: [
                MessageHandler(None, get_capdiametr),
            ],
            STEMHEIGHT: [
                MessageHandler(None, get_stemheight),
            ],
            STEMWIDTH: [
                MessageHandler(None, get_stemwidth),
            ],
            BRUISEBLEED: [
                MessageHandler(None, get_bruisebleed),
            ],
            HABITAT: [
                MessageHandler(None, get_habitat),
            ],
            SEASON: [
                MessageHandler(None, get_season),
            ],
            FINALACTION: [
                MessageHandler(None, get_finalaction),
            ],
            CANCEL: [
                MessageHandler(None, cancel),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

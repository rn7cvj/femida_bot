from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler , CallbackQueryHandler
from src.localization import TEXTS, CATEGORIES , DOCS # Импортируем тексты и категории
from src.sender import send_email

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

AGREEMENT, CATEGORY, SUBCATEGORY, REQUEST, START_OVER = range(5)

category_buttons = [
            [InlineKeyboardButton(category, callback_data=category)] for category in CATEGORIES.keys()
        ]

agreement_buttons = [
    [
        InlineKeyboardButton(TEXTS["agreement_buttons"]["agree"], callback_data="agree"),
        InlineKeyboardButton(TEXTS["agreement_buttons"]["disagree"], callback_data="disagree")
    ]
]

# Функция /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        TEXTS["start_message"],
        reply_markup=InlineKeyboardMarkup(agreement_buttons)
    )
    
    return AGREEMENT
    

# Функция обработки согласия
async def agreement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    user_reply = query.data

    if user_reply == "agree":
        # Отправляем отдельное сообщение с согласием
        await query.edit_message_text(TEXTS["agree_message"])
        
        # Отправляем сообщение с выбором категории
        await query.message.reply_text(
            TEXTS["choose_category"],
            reply_markup=InlineKeyboardMarkup(category_buttons)
        )
        return CATEGORY
    
    if user_reply == "disagree":
        await query.edit_message_text(TEXTS["disagree_message"])
        return ConversationHandler.END

    return ConversationHandler.END

# Функция обработки выбора категории
async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    category = query.data
    
    if category in CATEGORIES:

        category_index = list(CATEGORIES.keys()).index(category)

        subcategory_buttons = [
            [
                InlineKeyboardButton(subcategory, callback_data=str(category_index) + ":" + str(CATEGORIES[category].index(subcategory)) ),
             ] for subcategory in CATEGORIES[category]
        ]
        subcategory_buttons.append([InlineKeyboardButton(TEXTS['back'], callback_data="back_to_category")])
        

        await query.edit_message_text(
            TEXTS["choose_subcategory"].replace("%% CATEGORY_NAME %%", category),
            reply_markup=InlineKeyboardMarkup(subcategory_buttons)
        )
        return SUBCATEGORY

    await query.edit_message_text(TEXTS["error_category"])
    return CATEGORY

# Функция обработки выбора подкатегории
async def subcategory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data


    if data == "back_to_category":
        category_buttons = [
                [InlineKeyboardButton(category, callback_data=category)] for category in CATEGORIES.keys()      
            ]   
        await query.edit_message_text(TEXTS["choose_category"], reply_markup=InlineKeyboardMarkup(category_buttons))
        return CATEGORY

    subcategory_index = int(data.split(":")[1])
    category_index = int(data.split(":")[0])

    category = list(CATEGORIES.keys())[category_index]

    subcategory = CATEGORIES[category][subcategory_index]

    if category == "Документация":

        file_path = DOCS[subcategory]

        await query.message.delete()

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(file_path, 'rb'),
            caption=TEXTS["document_caption"].replace("%% SUBCATEGORY_NAME %%", subcategory),
            filename=TEXTS["document_caption"].replace("%% SUBCATEGORY_NAME %%", subcategory)
        )
        
        category_buttons = [
            [InlineKeyboardButton(category, callback_data=category)] for category in CATEGORIES.keys()
        ]

        await query.message.reply_text(
            text=TEXTS["choose_category"],
            reply_markup=InlineKeyboardMarkup(category_buttons)
        )

        return CATEGORY


    await query.edit_message_text(TEXTS["request_instructions"].replace("%% CATEGORY_NAME %%", category).replace("%% SUBCATEGORY_NAME %%", subcategory))
    return REQUEST

# Функция обработки файла запроса
async def request_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    file = update.message.document
    query = update.callback_query

    if file:
        try:

            message = await update.message.reply_text(
                TEXTS["file_in_process"],
            )

            file = await file.get_file()

            file_path = f"./downloads/{file.file_id}.{file.file_path.split('.')[-1]}"
        

            await file.download_to_drive(
                custom_path=file_path
            )
        

            send_email(
                subject="Запрос на юридическую консультацию",
                body="Пожалуйста, ознакомьтесь с прикрепленным файлом.",
                attachment_path=file_path
            )

            start_over_button = [
                [InlineKeyboardButton(TEXTS["start_over"], callback_data="start_over")]
            ]

            # await update.message.delete()


            # await update.callback_query.edit_message_text(
            #     TEXTS["file_received"],
            #     reply_markup=InlineKeyboardMarkup(start_over_button)
            # )

            await message.edit_text(TEXTS["file_received"], reply_markup=InlineKeyboardMarkup(start_over_button),)

            os.remove(file_path)
        except Exception as e:
            print(e)
            await update.message.reply_text(TEXTS["file_received_fail"])
        
        
        return START_OVER
    else:
        await update.message.reply_text(TEXTS["file_error"])
        return REQUEST

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        TEXTS["choose_category"],  
        reply_markup=InlineKeyboardMarkup(category_buttons),)
    return CATEGORY

# Основная функция
def main():


    application = Application.builder().token(TOKEN).build()

    # Conversation handler для работы с шагами
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGREEMENT: [CallbackQueryHandler(agreement)],
            CATEGORY: [CallbackQueryHandler(category)],
            SUBCATEGORY: [CallbackQueryHandler(subcategory)],
            REQUEST: [MessageHandler(filters.Document.ALL & ~filters.COMMAND, request_file)],
            START_OVER : [CallbackQueryHandler(start_over)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

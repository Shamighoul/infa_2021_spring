import logging # импортируем логи
import config
count=0
global count
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update # Update - уже рассматривали
# Также импортируем кнопки
from telegram.ext import ( # дополнительно импортируем обработчик бесед
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Вкл. логи
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ans1, ans2, ans3, ans4, ans5 = range(5) # инициируем пол, фото, место и статус числами от 0 до 3.


def question_1(update: Update, context: CallbackContext) -> int: # возвращает целое число

    reply_keyboard = [['Да', 'Нет'],['Только солёные', 'Только сладкие']] # три кнопки в ряд

    update.message.reply_text(
        'Hi! My name is Bibi Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Ты любишь пироги??',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return ans1


def question_2(update: Update, context: CallbackContext) -> int:
    """Записывает пол в лог, спрашивает фото"""
    user = update.message.from_user # извлекли информацию о пользователе
    logger.info("ans1 of %s: %s", user.first_name, update.message.text) # записали в лог
    
    reply_keyboard = [['Да', 'Нет'],['Только подвижные игры', 'Только настольные игры']] # три кнопки в ряд
    
    update.message.reply_text( # отправляем сообщение
        'Ты любишь играть?? ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        
    )

    return ans2


def question_3(update: Update, context: CallbackContext) -> int:
    """Сохраняет фото и спрашивает место"""
    user = update.message.from_user # извлекли информацию о пользователе
    logger.info("ans2 of %s: %s", user.first_name, update.message.text) # записали в лог
    
    reply_keyboard = [['Да', 'Нет'],['Иногда', 'Почти никогда']] # три кнопки в ряд
    
    update.message.reply_text(
        ' Ты пользуешься косметикой?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return ans3


def question_4(update: Update, context: CallbackContext) -> int:
    """Сохраняем место и спрашиваем статус"""
    user = update.message.from_user
    logger.info("ans3 of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['Да', 'Нет'],['Иногда да', 'Почти никогда']] # три кнопки в ряд
    
    update.message.reply_text(
        'Ты любишь учиться?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return ans4

def question_5(update: Update, context: CallbackContext) -> int:
    """Сохраняем место и спрашиваем статус"""
    user = update.message.from_user
    logger.info("ans4 of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['Да', 'Нет'],['Иногда да', 'Почти никогда']] # три кнопки в ряд
    
    update.message.reply_text(
        'Ты романтик?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return ans5



def bio(update: Update, context: CallbackContext) -> int:
    """Получаем статус, сохраняем и прощаемся"""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    
    update.message.reply_text('Спасибо, что учавствовали в нашем вопросе, к сожалению получилось что вы смурфик, а не смешарик')
    reply_markup=ReplyKeyboardRemove(), # убрать
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Пишем в лог завершение разговора и прощаемся"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Пока, я буду ждать твоего возвращения', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Передаём токен в Updater.
    TOKEN = config.token
    updater = Updater(TOKEN)

    # Используем диспетчер для обработчиков
    dispatcher = updater.dispatcher

    # Добавляем обработчки беседы с состояниями GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', question_1)],
        states={ # Сопоставляем состояниям значения
            ans1: [MessageHandler(Filters.regex('^(Да|Нет|Только солёные|Только сладкие)$'), question_2)],
            ans2: [MessageHandler(Filters.regex('^(Да|Нет|Только подвижные игры|Только настольные игры)$'), question_3)],
            ans3: [
                MessageHandler(Filters.regex('^(Да|Нет|Иногда|Почти никогда)$'), question_4)],
            ans4: [MessageHandler(Filters.regex('^(Да|Нет|Иногда да|Почти никогда)$'), question_5)],
            ans5: [MessageHandler(Filters.text & ~Filters.command, bio)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler) # добавили обработчик беседы

    # Запустили бот
    updater.start_polling() 

    # Бот работает до Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

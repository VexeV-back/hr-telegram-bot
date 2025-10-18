import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# База знаний
KNOWLEDGE_BASE = {
    "отпуск": "Для оформления ежегодного оплачиваемого отпуска вам необходимо:\n1. Не менее чем за 2 недели до начала отпуска подать заявление вашему непосредственному руководителю.\n2. После согласования с руководителем, заявление передается в отдел кадров.\n3. Отдел кадров издаст приказ, с которым вас обязаны ознакомить под подпись.\n4. Отпускные должны быть выплачены не позднее, чем за 3 дня до начала отпуска.",
    
    "больничный": "Если вы заболели:\n1. В первый день болезни необходимо уведомить вашего непосредственного руководителя.\n2. Обратитесь в медицинское учреждение для получения листка нетрудоспособности (больничного).\n3. В день выхода на работу предоставьте оригинал больничного листа в отдел кадров.\n4. Пособие по временной нетрудоспособности будет выплачено в ближайший день зарплаты.",
    
    "льготы": "Наша компания предоставляет следующие корпоративные льготы:\n• Добровольное медицинское страхование (ДМС) для вас и ваших детей.\n• Компенсация 50% стоимости абонемента в спортивный зал (до 5000 руб. в год).\n• Организованное льготное питание в столовой компании.\n• Корпоративная скидка на продукты компании.\nПодробности уточняйте в отделе кадров.",
    
    "документы": "Для получения справок (2-НДФЛ, о зарплате, с места работы) или заверенной копии трудовой книжки необходимо написать заявление в отдел кадров. Обычно документы готовятся в течение 3 рабочих дней.",
    
    "отгул": "Для оформления отгула (отпуска за свой счет):\nПодайте заявление на имя руководителя с указанием причины и дат.",
    
    "удаленка": "Для оформления удаленной работы:\nНеобходимо согласовать с руководителем и подписать дополнительное соглашение к договору в отделе кадров."
}

# Ключевые слова для каждого intent
KEYWORDS = {
    "отпуск": ["отпуск", "отдых", "отпускные", "отгул", "заявление на отпуск"],
    "больничный": ["больничный", "заболел", "болею", "листок нетрудоспособности", "больничный лист"],
    "льготы": ["льготы", "бенефиты", "дмс", "страхование", "спортзал", "питание", "скидка"],
    "документы": ["документы", "справка", "2-ндфл", "трудовая книжка", "копия трудовой"],
    "отгул": ["отгул", "за свой счет", "отпуск без содержания"],
    "удаленка": ["удаленка", "удаленная работа", "из дома", "дистанционно"]
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
👋 Здравствуйте! Я ваш виртуальный помощник по кадровым вопросам.

Я могу помочь с вопросами по следующим темам:
• 📅 Отпуск и отгулы
• 🏥 Больничные листы  
• 💼 Корпоративные льготы (ДМС, спортзал, питание)
• 📄 Оформление документов
• 🏠 Удаленная работа

Просто напишите ваш вопрос, например: "Как оформить отпуск?" или "Какие есть льготы?"
    """
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📋 Доступные команды:
/start - Начать работу
/help - Получить справку
/vacation - Информация об отпуске
/sick_leave - Информация о больничном
/benefits - Корпоративные льготы
/documents - Оформление документов

Или просто задайте ваш вопрос в свободной форме!
    """
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text.lower()
    
    # Определяем тему вопроса по ключевым словам
    found_topic = None
    for topic, keywords in KEYWORDS.items():
        if any(keyword in user_message for keyword in keywords):
            found_topic = topic
            break
    
    if found_topic:
        # Нашли подходящую тему - даем ответ
        response = KNOWLEDGE_BASE.get(found_topic, "Извините, информация по этому вопросу временно недоступна.")
    else:
        # Не нашли тему - даем общий ответ
        response = "Извините, я не совсем понял ваш вопрос. Пожалуйста, уточните его. Я могу помочь с вопросами об отпуске, больничных, льготах и документах."
    
    await update.message.reply_text(response)

async def vacation_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /vacation"""
    await update.message.reply_text(KNOWLEDGE_BASE["отпуск"])

async def sick_leave_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /sick_leave"""
    await update.message.reply_text(KNOWLEDGE_BASE["больничный"])

async def benefits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /benefits"""
    await update.message.reply_text(KNOWLEDGE_BASE["льготы"])

async def documents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /documents"""
    await update.message.reply_text(KNOWLEDGE_BASE["документы"])

def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("vacation", vacation_command))
    application.add_handler(CommandHandler("sick_leave", sick_leave_command))
    application.add_handler(CommandHandler("benefits", benefits_command))
    application.add_handler(CommandHandler("documents", documents_command))
    
    # Добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("🚀 Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()

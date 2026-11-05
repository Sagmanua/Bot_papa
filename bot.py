import telebot
from telebot import types
import json
import os
import glob
from telebot import apihelper
import re

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# Global state
questions_data = []
current_file = None

# Define database directory
DATABASE_DIR = 'database'

def get_main_menu():
    """Creates a permanent reply keyboard at the bottom of the screen"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📂 Choose Database File"))
    return markup

def load_json_file(filename):
    global questions_data, current_file
    # Construct full path to the file inside the database folder
    file_path = os.path.join(DATABASE_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
            current_file = filename
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "Привіт! Я готовий до пошуку. Скористайтеся кнопкою нижче, щоб обрати файл.",
        reply_markup=get_main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "📂 Choose Database File")
def show_file_selection(message):
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR, exist_ok=True)
        bot.reply_to(message, f"Папка '{DATABASE_DIR}' була створена. Додайте туди файли `data_*.json`.")
        return

    search_pattern = os.path.join(DATABASE_DIR, 'data_*.json')
    files = glob.glob(search_pattern)
    
    if not files:
        bot.reply_to(message, f"Файли `data_*.json` не знайдені в папці `{DATABASE_DIR}/`.")
        return

    # Sort files naturally by the number inside their filename
    def natural_sort_key(file_path):
        filename = os.path.basename(file_path)
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else 0

    sorted_files = sorted(files, key=natural_sort_key)

    markup = types.InlineKeyboardMarkup()
    for file_path in sorted_files:
        file_name = os.path.basename(file_path)
        button = types.InlineKeyboardButton(text=f"📄 {file_name}", callback_data=f"select_{file_name}")
        markup.add(button)
    
    bot.send_message(message.chat.id, "Оберіть базу даних для пошуку:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_'))
def handle_selection(call):
    file_to_load = call.data.replace('select_', '')
    
    if load_json_file(file_to_load):
        bot.answer_callback_query(call.id, f"Активовано: {file_to_load}")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ **Поточний файл:** `{file_to_load}` (з папки `{DATABASE_DIR}/`)\nЗнайдено питань: {len(questions_data)}\n\nПросто напишіть текст для пошуку.",
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "Помилка завантаження.")

@bot.message_handler(func=lambda message: True)
def search_handler(message):
    global questions_data, current_file
    
    if not questions_data:
        bot.reply_to(message, "Спочатку оберіть файл через меню нижче 👇")
        show_file_selection(message)
        return

    query = message.text.lower()
    results = [q for q in questions_data if query in q.get('question', '').lower()]

    if not results:
        bot.reply_to(message, f"Нічого не знайдено у файлі `{current_file}`.")
        return

    for item in results[:5]:
        question_text = item.get('question', 'Без назви')
        response = f"📌 **{question_text}**\n\n"
        
        for opt in item.get('options', []):
            text = opt.get('text', '')
            response += f"✅ *{text}*\n" if opt.get('is_correct') else f"▫️ {text}\n"
        
        bot.send_message(message.chat.id, response, parse_mode="Markdown")

if __name__ == '__main__':
    print("Бот працює...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
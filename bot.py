import telebot
import requests
import os

TOKEN = os.getenv('TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

bot = telebot.TeleBot(TOKEN)

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Привет! Я Grok 4 + GPT-4o + Claude 3.5\n"
        "Просто напиши любой вопрос — отвечу самой новой моделью 2025 года 🚀\n\n"
        "Подписка: /pay")

# Все остальные сообщения → отправляем в OpenRouter
@bot.message_handler(func=lambda message: True)
def answer(message):
    if not OPENROUTER_API_KEY:
        bot.reply_to(message, "Ошибка: нет ключа OpenRouter")
        return

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    data = {
        "model": "openai/gpt-4o",           # можно менять на grok-4, claude-3.5-sonnet и т.д.
        "messages": [{"role": "user", "content": message.text}]
    }
    try:
        r = requests.post(url, json=data, headers=headers, timeout=60)
        answer = r.json()['choices'][0]['message']['content']
        bot.reply_to(message, answer)
    except:
        bot.reply_to(message, "Извини, сейчас не могу ответить. Попробуй чуть позже.")

# Команда оплаты (пока просто заглушка)
@bot.message_handler(commands=['pay'])
def pay(message):
    bot.send_message(message.chat.id,
        "Тарифы:\n7 дней — 299 ₽\n30 дней — 699 ₽\nНавсегда — 1690 ₽\n\n"
        "Оплата через @CryptoBot или ЮKassa — скоро подключу!")

print("Бот запущен!")
bot.polling(none_stop=True)

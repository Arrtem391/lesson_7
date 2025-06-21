import os
from dotenv import load_dotenv
import ptbot
from pytimeparse import parse

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def send_initial_message(chat_id, seconds, bot_instance):
    return bot_instance.send_message(chat_id, f"Осталось {seconds} секунд\n{render_progressbar(seconds, seconds)}")

def update_message(secs_left, chat_id, message_id, total_seconds, bot_instance):
    progress_bar = render_progressbar(total_seconds, total_seconds - secs_left)
    try:
        bot_instance.update_message(chat_id, message_id, f"Осталось {secs_left} секунд\n{progress_bar}")
    except Exception:
        pass
    
    if secs_left == 0:
        bot_instance.send_message(chat_id, "Время вышло!")

def wait_handler(chat_id, message, bot_instance):
    seconds = parse(message)
    if not seconds:
        bot_instance.send_message(chat_id, "Неверный формат времени. Используйте например '5s' или '1m'")
        return
    
    message_id = send_initial_message(chat_id, seconds, bot_instance)
    update_message(seconds, chat_id, message_id, seconds, bot_instance)
    bot_instance.create_countdown(
        seconds,
        update_message,
        chat_id=chat_id,
        message_id=message_id,
        total_seconds=seconds,
        bot_instance=bot_instance
    )

def main():
    load_dotenv()
    tg_token = os.getenv('T_TOKEN')

    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait_handler, bot_instance=bot)
    bot.run_bot()

if __name__ == '__main__':
    main()

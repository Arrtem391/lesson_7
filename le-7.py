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


def make_wait_handler(bot_instance):
    def wait(chat_id, message):
        seconds = parse(message)
        if not seconds:
            bot_instance.send_message(chat_id, "Неверный формат времени. Используйте например '5s' или '1m'")
            return
        
        message_id = bot_instance.send_message(chat_id, f"Осталось {seconds} секунд\n{render_progressbar(seconds, seconds)}")
        
        def update_message(secs_left):
            progress_bar = render_progressbar(seconds, seconds - secs_left)
            bot_instance.update_message(chat_id, message_id, f"Осталось {secs_left} секунд\n{progress_bar}")
            
            if secs_left == 0:
                bot_instance.send_message(chat_id, "Время вышло!")
        
        update_message(seconds)
        bot_instance.create_countdown(seconds, update_message)
    
    return wait


def main():
    load_dotenv()
    tg_token = os.getenv('T_TOKEN')
    tg_chat_id = os.getenv('T_CHAT_ID')

    bot = ptbot.Bot(tg_token)
    wait_handler = make_wait_handler(bot)
    bot.reply_on_message(wait_handler)
    bot.send_message(tg_chat_id, "Бот запущен. Отправьте время для отсчёта (например, '5s' или '1m')")
    bot.run_bot()


if __name__ == '__main__':
    main()

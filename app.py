from signal import signal, SIGINT, SIGTERM

from bot.bot import Bot

# Start if main script
if __name__ == '__main__':
    bot = Bot()
    bot.start()

    signal(SIGINT, bot.stop)
    signal(SIGTERM, bot.stop)

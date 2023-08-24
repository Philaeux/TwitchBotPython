import multiprocessing

from bot.bot import Bot

if __name__ == '__main__':
    multiprocessing.freeze_support()
    Bot().run()

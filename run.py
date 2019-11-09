import sys

from cybogram import Cybogram

if __name__ == '__main__':
    bot = Cybogram()
    bot.start(account=sys.argv[1])

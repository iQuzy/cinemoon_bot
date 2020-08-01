from lib.handler import Handler
from lib.hdvbDriver import HDVB
from aiogram import Bot

import config

bot = Bot(token=config.BOT_TOKEN)
hl = Handler('db/handler.db')
hdvb = HDVB(config.HDVD_TOKEN, 'db/hdvb.db')

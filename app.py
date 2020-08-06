from lib.handler import Handler
from lib.hdvbDriver import HDVB
from aiogram import Bot

import config

bot = Bot(token=config.BOT_TOKEN)
hl = Handler('db/handler.db')
hdvb = HDVB(hdvb_token=config.HDVD_TOKEN, kp_token=config.KP_TOKEN, dbpath='db/hdvb.db')

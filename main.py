import asyncio
from DiscordFront.discord_front import bot
from config import settings
from Models.discord_model import update_balance


bot.run(settings.BOT_TOKEN)

from Models.discord_model import create_tables,insert_data
from DiscordFront.discord_front import bot
from config import settings


bot.run(settings.BOT_TOKEN)

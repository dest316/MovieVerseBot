import discord
from discord.ext import commands
from discord import app_commands
from Models.discord_model import update_balance


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)


async def sync_command(bot, guild):
    await bot.tree.sync(guild=guild)


@bot.event
async def on_ready():
    guild = discord.Object(id="1259441070740344933")
    bot.tree.copy_global_to(guild=guild)
    await sync_command(bot, guild)
    print("sync")


@bot.tree.command(name="add_rolls", description="Добавить рулеты участнику")
async def add_rolls(interaction: discord.Interaction, user: str, amount: int):
    try:
        username = user
    except ValueError:
        await interaction.response.send_message("Укажите имя пользователя и тег в формате username#1234")
        return
    member = discord.utils.get(interaction.guild.members, name=username)
    if member is None:
        await interaction.response.send_message(f"Пользователь {user} не найден")
        return
    discord_id = member.id
    await update_balance(str(discord_id), amount)
    await interaction.response.send_message(discord_id)
import discord
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)


async def sync_command(bot):
    await bot.tree.sync()


@bot.event
async def on_ready():
    await sync_command(bot)


@bot.tree.command(name="add_rolls", description="Добавить рулеты участнику")
async def add_rolls(ctx, user: str, amount: int):
    try:
        username, discriminator = user.split('#')
    except ValueError:
        await ctx.send("Укажите имя пользователя и тег в формате username#1234")
        return
    member = discord.utils.get(ctx.guild.members, name=username, discriminator=discriminator)
    if member is None:
        await ctx.send(f"Пользователь {user} не найден")
        return
    discord_id = member.id
    await ctx.send(discord_id)
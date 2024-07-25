import discord
from discord.ext import commands
from discord import app_commands
from Models.discord_model import update_balance, get_balance, roll_transfer
from utils import get_rolls_word, TransferStatus
from math import ceil
from discord.ui import Button, View


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


@bot.tree.command(name="change_rolls", description="Изменить баланс участника на amount рулетов. При указании "
                                                   "отрицательного значения валюта вычтется.")
async def add_rolls(interaction: discord.Interaction, user: str, amount: int):
    member = discord.utils.get(interaction.guild.members, name=user)
    if member is None:
        await interaction.response.send_message(f"Пользователь с идентификатором {user} не найден на сервере", ephemeral=True)
        return
    discord_id = member.id
    await update_balance(str(discord_id), amount)
    await interaction.response.send_message(f"Баланс {user} {'увеличен' if amount >= 0 else 'уменьшен'} на {amount} {get_rolls_word(amount)}.", ephemeral=True)


@bot.tree.command(name="my_balance", description="Посмотреть свой баланс рулетов")
async def check_balance(interaction: discord.Interaction):
    member_id = interaction.user.id
    balance = await get_balance(str(member_id))
    await interaction.response.send_message(f"Ваш баланс равен {balance} {get_rolls_word(balance)}", ephemeral=True)


@bot.tree.command(name="trade", description="Отправить рулеты другому участнику сервера")
async def roll_trade(interaction: discord.Interaction, recipient: str, amount: int):
    SERVICE_COMMISSION = 0.2
    if amount < 2:
        await interaction.response.send_message(f"Сумма трансфера не может быть меньше, чем 2 рулета", ephemeral=True)
        return
    commission = ceil(amount * SERVICE_COMMISSION)
    total_amount = commission + amount
    embed = discord.Embed(title="Подтверждение перевода", description=f"Вы собираетесь перевести {amount} {get_rolls_word(amount)} пользователю {recipient}. Комиссия за операцию составит {commission} {get_rolls_word(commission)}. Общая сумма платежа: {total_amount} {get_rolls_word(total_amount)}. Подтвердите операцию.", color=discord.Color.blue())
    confirm_button = Button(label="Подтвердить", style=discord.ButtonStyle.green)
    cancel_button = Button(label="Отменить", style=discord.ButtonStyle.red)

    async def confirm_callback(inner_interaction: discord.Interaction):
        sender_user_id = str(inner_interaction.user.id)
        recipient_user = discord.utils.get(interaction.guild.members, name=recipient)
        if not recipient_user:
            await interaction.response.send_message("На данном сервере нет пользователя с таким идентификатором")
        else:
            recipient_user_id = str(recipient_user.id)
            operation_status_code = await roll_transfer(sender_user_id, recipient_user_id, amount, total_amount)
            await interaction.edit_original_response(embed=embed, view=None)
            await interaction.followup.send(TransferStatus().statuses[operation_status_code], ephemeral=True)

    async def cancel_callback(inner_interaction: discord.Interaction):
        await interaction.edit_original_response(embed=embed, view=None)
        await inner_interaction.response.send_message("Операция отменена.", ephemeral=True)

    confirm_button.callback = confirm_callback
    cancel_button.callback = cancel_callback

    view = View(timeout=5)
    view.add_item(confirm_button)
    view.add_item(cancel_button)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.tree.command(name="set_balance", description="Делает баланс пользователя равным amount")
async def set_balance(interaction: discord.Interaction, user: str, amount: int):
    member = discord.utils.get(interaction.guild.members, name=user)
    if member is None:
        await interaction.response.send_message(f"Пользователь с идентификатором {user} не найден на сервере", ephemeral=True)
        return
    discord_id = member.id
    await update_balance(str(discord_id), amount, is_absolute_assignment=True)
    await interaction.response.send_message(
        f"Баланс {user} равен {amount} {get_rolls_word(amount)}.",
        ephemeral=True)


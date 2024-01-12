import logging
import random
import time
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
import asyncio
from logging.handlers import RotatingFileHandler
import random  # Import random module

api_id = 3748059
api_hash = "f8c9df448f3ba20a900bc2ffc8dae9d5"
chat_id = -1002137560330
channel_id = ["@DiveMarketPlace"]
mp_link = "https://t.me/+oVqB_bTso2VjNmU9"
allow_id = "6162272468"
max_posts = 4
max_time = 600
session_string = "BQCwmCUAHFk47MqjDKFvwesq4LEA4sJfyYZv-jK1-oA9eJkAsQyVzjOfbQ1vjTcaGY9ECwbSzKw3I0gkhqnJqsvPZ-dYeXdW-1YuAoBSie-hC1vabp_NG08U9sMGhRIJP6A8eFzljPHLjKC2PrQ37ZFrJUmqpJPx68_EsEoTjL1IjOzjgpjYdGC4J40J3EyrXlk0tri3CMGMWxqyHtCHmBOpPsWTEpASQI8X2FLmIrQPxXSof-huvvmmsUpdrbvnsYoexQOk_9WDads40qmv3fYvpFxjOygJMsUZGbk3py-6GXd33Y-pI4Ul7sWbC2jnR3vgAVmeRD66JWFb30Wa4RSIXXb2YQAAAAGKNpGvAA"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGS = logging.getLogger()

# =========== Client =========== #

bot = Client(
    "client",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session_string,
)

last_message_times = {}
user_message_count = {}
allowed_user_id = allow_id.split(" ")

@bot.on_message(filters.command(["start"]) & ~filters.bot)
async def start_handler(bot: Client, message: Message):
    await message.reply("Click the button below to join the #Official Marketplace", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join channel", url=f"{mp_link}")]]))

@bot.on_message(filters.chat(chat_id) & ~filters.bot)
async def forward_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    reply_id = message.reply_to_message.from_user.id
    count_value = total_limit_id()
    if is_id_limit(user_id):
        max_posts_per_day = count_value[user_id]
    else:
        max_posts_per_day = max_posts
    if message.text == "/sub":
        if message.reply_to_message:
            if user_message_count.get(reply_id, 0) >= max_posts_per_day:
                remaining_posts = 0
            else:
                remaining_posts = max_posts_per_day - user_message_count.get(reply_id, 0)
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(reply_id, 0)}"
            return await message.reply_text(remaining_posts_message)
        else:
            if user_message_count.get(user_id, 0) >= max_posts_per_day:
                remaining_posts = 0
            else:
                remaining_posts = int(max_posts_per_day) - user_message_count.get(user_id, 0)
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(user_id, 0)}"
            return await message.reply_text(remaining_posts_message)
    if message.text.startswith('.') or message.text.startswith('/'):
        return
    if user_id in last_message_times:
        if str(user_id) in str(allowed_user_id):
            last_message_times[user_id] = time.time()
        else:
            if user_message_count.get(user_id, 0) >= max_posts_per_day:
                return await message.reply_text("Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit.")
        time_since_last_message = time.time() - last_message_times[user_id]
        if time_since_last_message < int(max_time):
            remaining_time = int(max_time) - time_since_last_message
            cooldown_message = f"Please wait {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds before posting another message to the channel.\n\n**Your post is added to queue & will be posted after {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds automatically.**"
            await message.reply_text(cooldown_message)
            await asyncio.sleep(remaining_time)
            if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                return await message.reply_text("Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit.")
            last_message_times[user_id] = time.time()
            for id in channel_id:
                await bot.forward_messages(id, message.chat.id, message.message_id)
                await asyncio.sleep(random.randint(1, 4))
            user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
            return
    last_message_times[user_id] = time.time()
    for id in channel_id:
        await bot.forward_messages(id, message.chat.id, message.message_id)
        await asyncio.sleep(random.randint(1, 4))
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1

async def start_bot():
    await bot.start()
    lol = await bot.get_me()
    await bot.send_photo(chat_id, "https://telegra.ph/file/2707a66c92ba3c2e40cee.jpg", f"#START\n\nVersion:- α • 1.1\n\nYour Market Place Bot Has Been Started Successfully")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

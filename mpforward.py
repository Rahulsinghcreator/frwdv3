import asyncio
import logging
import random  # Import random module
import time
from logging.handlers import RotatingFileHandler

from pyrogram import Client, filters, idle
from pyrogram.types import Message

from Config import *
from limit import *

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
    await message.reply("I am alive")


@bot.on_message(filters.command(["limit"]) & ~filters.bot & filters.me)
async def start_handler(bot: Client, message: Message):
    tmsg = message.text.split(" ")
    count = tmsg[1]
    reply_id = (
        message.reply_to_message.from_user.id if message.reply_to_message else None
    )
    if reply_id:
        add_limit(reply_id, count)
        await message.reply(
            f"Successfully set limit\n**Chat id**: {reply_id}\n**Limit**: {count}"
        )
    await message.reply("Reply to him message and use command \n`/limit <value>")


@bot.on_message(filters.chat(chat_id) & ~filters.bot)
async def forward_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    reply_id = (
        message.reply_to_message.from_user.id if message.reply_to_message else None
    )
    count_value = total_limit_id()
    if is_id_limit(user_id):
        max_posts_per_day = count_value[user_id]
    else:
        max_posts_per_day = max_posts
    if message.text == "/sub":
        if reply_id:
            if user_message_count.get(reply_id, 0) >= max_posts_per_day:
                remaining_posts = 0
            else:
                remaining_posts = max_posts_per_day - user_message_count.get(
                    reply_id, 0
                )
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(reply_id, 0)}"
            return await message.reply_text(remaining_posts_message)
        else:
            if user_message_count.get(user_id, 0) >= max_posts_per_day:
                remaining_posts = 0
            else:
                remaining_posts = int(max_posts_per_day) - user_message_count.get(
                    user_id, 0
                )
            remaining_posts_message = f"• Remaining Post :{remaining_posts} out of {max_posts_per_day} posts today\n\n• Total Posted = {user_message_count.get(user_id, 0)}"
            return await message.reply_text(remaining_posts_message)
    if message.text.startswith(".") or message.text.startswith("/"):
        return
    if user_id in last_message_times:
        if str(user_id) in str(allowed_user_id):
            last_message_times[user_id] = time.time()
        else:
            if user_message_count.get(user_id, 0) >= max_posts_per_day:
                return await message.reply_text(
                    "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                )
        time_since_last_message = time.time() - last_message_times[user_id]
        if time_since_last_message < int(max_time):
            remaining_time = int(max_time) - time_since_last_message
            cooldown_message = f"Please wait {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds before posting another message to the channel.\n\n**Your post is added to queue & will be posted after {int(remaining_time / 60)} minutes & {int(remaining_time % 60)} seconds automatically.**"
            await message.reply_text(cooldown_message)
            await asyncio.sleep(remaining_time)
            if user_message_count.get(user_id, 0) >= int(max_posts_per_day):
                return await message.reply_text(
                    "Today's Post Limit Exceeded !!!\n\nYou've now no posts left in your daily sub - wait 12 hours to refresh the post limit."
                )
            last_message_times[user_id] = time.time()
            for id in channel_id:
                await bot.forward_messages(id, message.chat.id, message.id)
                await asyncio.sleep(random.randint(1, 4))
            user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
            return
    last_message_times[user_id] = time.time()
    for id in channel_id:
        await bot.forward_messages(id, message.chat.id, message.id)
        await asyncio.sleep(random.randint(1, 4))
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1


async def start_bot():
    await bot.start()
    await bot.get_me()
    await bot.send_photo(
        chat_id,
        "https://telegra.ph/file/2707a66c92ba3c2e40cee.jpg",
        f"#START\n\nVersion:- α • 1.1\n\nYour Market Place Bot Has Been Started Successfully",
    )
    await idle()


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

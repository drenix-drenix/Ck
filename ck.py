import asyncio
import regex as re
from telethon import TelegramClient, events

api_id = 23652918  # ваш апи айди
api_hash = 'fdfefb9dde5b0edd59d349b64901dc3a'  # ваш апи ключ

client = TelegramClient(session='session', api_id=api_id, api_hash=api_hash, system_version="4.16.30-vxSOSYNXA ")
client.start()

code_regex = re.compile(r"t\.me/wallet\?start=(CQ[A-Za-z0-9]{10}|C-[A-Za-z0-9]{10}|t_[A-Za-z0-9]{15}|[A-Za-z]{12})", re.IGNORECASE)

replace_chars = ''' @#&+()*"'…;,!№•—–·±<{>}†★‡„“”«»‚‘’‹›¡¿‽~`|√π÷×§∆\\°^%©®™✓₤$₼€₸₾₶฿₳₥₦₫₿¤₲₩₮¥₽₻₷₱₧£₨¢₠₣₢₺₵₡₹₴₯₰₪'''
translation = str.maketrans('', '', replace_chars)

crypto_black_list = [1985737506]

async def subscribe_and_activate_code(bot_name, code):
    # Получаем информацию о канале
    channel_info = await client.get_entity(bot_name)
    
    # Подписываемся на канал
    await client(JoinChannelRequest(channel_info))
    
    # Активируем чек
    await client.send_message(bot_name, message=f'/start {code}')

@client.on(events.MessageEdited(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
@client.on(events.NewMessage(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
async def handle_new_message(event):
    message_text = event.message.text.translate(translation)
    codes = code_regex.findall(message_text)
    if codes:
        for bot_name, code in codes:
            # Вызываем функцию для подписки и активации чека
            await subscribe_and_activate_code(bot_name, code)
    try:
        for row in event.message.reply_markup.rows:
            for button in row.buttons:
                try:
                    match = code_regex.search(button.url)
                    if match:
                        # Вызываем функцию для подписки и активации чека
                        await subscribe_and_activate_code(match.group(1), match.group(2))
                except AttributeError:
                    pass
    except AttributeError:
        pass

client.run_until_disconnected()

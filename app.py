import os

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')


client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    #
    dialogs = await client.get_dialogs()
    for dialog in dialogs:


        async for message in client.iter_messages(dialog):
            if message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    print(f"Message contains an image: {message.media}")
                    await message.download_media()

                elif isinstance(message.media, MessageMediaDocument):
                    print(f"Message contains a document or other file: {message.media.document}")
                    await message.download_media()

            else:
                print(f"Text Message: {message.text}")

with client:
    client.loop.run_until_complete(main())
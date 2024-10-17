import os

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, DocumentAttributeFilename, \
    DocumentAttributeImageSize, PhotoStrippedSize
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')


client = TelegramClient('session_name', api_id, api_hash)

async def get_messages_from_dialog(dialog_name=None, dialog_id=None):
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        if dialog_name and dialog.name == dialog_name:
            print(f"Fetching messages from {dialog.name}")
            await process_messages(dialog)

        elif dialog_id and dialog.id == dialog_id:
            print(f"Fetching messages from {dialog.name}")
            await process_messages(dialog)


async def process_messages(dialog):
    async for message in client.iter_messages(dialog):
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo_info = message.media.photo
                print(f"Message contains an image:")
                print(f" - Photo ID: {photo_info.id}")
                print(f" - Access Hash: {photo_info.access_hash}")
                print(f" - File Reference: {photo_info.file_reference}")
                print(f" - Date: {photo_info.date}")
                print(f" - DC ID: {photo_info.dc_id}")
                print(f" - Has Stickers: {photo_info.has_stickers}")
                print(
                    f" - Sizes: {[f'{size.w}x{size.h}' for size in photo_info.sizes if hasattr(size, 'w')]}")  # Only print sizes with width and height
                print(f" - Video Sizes: {photo_info.video_sizes if hasattr(photo_info, 'video_sizes') else 'N/A'}")

                await message.download_media()

            elif isinstance(message.media, MessageMediaDocument):
                document_info = message.media.document
                file_name = next(attr.file_name for attr in document_info.attributes if hasattr(attr, 'file_name'))

                print(f"Message contains a document or other file:")
                print(f" - Document ID: {document_info.id}")
                print(f" - Access Hash: {document_info.access_hash}")
                print(f" - File Reference: {document_info.file_reference}")
                print(f" - Date: {document_info.date}")
                print(f" - Mime Type: {document_info.mime_type}")
                print(f" - File Size: {document_info.size / 1024:.2f} KB")
                print(f" - DC ID: {document_info.dc_id}")

                for attr in document_info.attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        print(f" - File Name: {attr.file_name}")
                    elif isinstance(attr, DocumentAttributeImageSize):
                        print(f" - Image Size: {attr.w}x{attr.h}")

                if document_info.thumbs:
                    for thumb in document_info.thumbs:
                        if isinstance(thumb, PhotoStrippedSize):
                            print(f" - Stripped Thumbnail: (Raw Bytes Data: {len(thumb.bytes)} bytes)")
                        else:
                            print(
                                f" - Thumbnail: {thumb.type} - {thumb.w}x{thumb.h} (Size: {thumb.size if hasattr(thumb, 'size') else 'N/A'})")

                await message.download_media()
        else:
            print(f"Text Message: {message.text}")


async def main():
    await client.start(phone=phone_number)

    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        print(f"Dialog Name: {dialog.name}, Dialog ID: {dialog.id}")

    await get_messages_from_dialog(dialog_id=7185473942)


with client:
    client.loop.run_until_complete(main())
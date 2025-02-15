import os
import base64

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from utils import make_api_call

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me a message, and I'll process it with Qwen. It can be image and/or text")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message, image_url = '', ''

    if update.message.text:
        user_message = update.message.text
    elif update.message.caption:
        user_message = update.message.caption
    
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{base64_image}"
       
    response = await make_api_call(user_message, image_url)
    await update.message.reply_text(response)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.PHOTO, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8617365285:AAElJlDzHTS3AiRjHjO88vPPknpdKV17fok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("YouTube Music Bot အဆင်သင့်ဖြစ်ပါပြီ!\nYouTube Link ပို့ပေးပါ။")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url: return
    
    status_msg = await update.message.reply_text("ဒေါင်းလုဒ်ဆွဲနေပါပြီ... ခဏစောင့်ပါ။")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
        'nocheckcertificate': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as audio:
            await update.message.reply_audio(audio)
        os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
  

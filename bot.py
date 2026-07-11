import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

client=OpenAI(api_key=os.environ["GROQ_API_KEY"],base_url="https://api.groq.com/openai/v1")

SYSTEM="Ti je asistent gazetaresk. Rregullon tekste, përkthen dhe krijon tituj."

async def reply(update:Update, context:ContextTypes.DEFAULT_TYPE):
    r=client.chat.completions.create(
      model="llama-3.3-70b-versatile",
      messages=[{"role":"system","content":SYSTEM},
                {"role":"user","content":update.message.text}]
    )
    await update.message.reply_text(r.choices[0].message.content)

app=Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()

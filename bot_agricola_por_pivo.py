
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "7598005421:AAH6k74olIKhp8XQUVdrUgdrp77wPx9U_XU"
df = pd.read_csv("plantios_cenoura_completo.csv")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Digite o número do pivô que você quer informações (ex: pivô 21).")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    resposta = ""

    for numero in df['Pivô'].unique():
        if f"pivô {numero}".lower() in texto:
            infos = df[df['Pivô'] == numero]
            for i, row in infos.iterrows():
                resposta += f"📌 {row['Cultura']} - {row['Área']} ha - {row['Status']} - {row['Safra']}
"
            break

    if resposta == "":
        resposta = "Pivô não encontrado. Tente outro número."

    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Bot rodando...")
app.run_polling()

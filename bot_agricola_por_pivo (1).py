
import os
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

CSV_PATH = "plantios_cenoura_completo.csv"
df = pd.read_csv(CSV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Alisson Envie o número do pivô no formato: pivô 21, pivô 36, etc.\n"
        "E eu te trago todos os plantios associados a ele."
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()

    if texto.startswith("pivô"):
        numero = texto.replace("pivô", "").strip()
        encontrados = df[df["Pivô"].str.contains(numero)]

        if not encontrados.empty:
            resposta = ""
            for _, row in encontrados.iterrows():
                resposta += (
                    "✅ *PLS {}*\n"
                    "📍 Fazenda: {}\n"
                    "🌱 Cultura: Cenoura\n"
                    "📆 Plantio: {}\n"
                    "📐 Área: {} ha\n"
                    "💧 Pivô: {}\n"
                    "🌤️ Subsafra: {}\n"
                    "🔁 Ciclo: {} dias\n\n"
                ).format(
                    row['Código PLS'], row['Fazenda'], row['Data de Plantio'],
                    row['Área (ha)'], row['Pivô'], row['Subsafra'], row['Ciclo (dias)']
                )
        else:
            resposta = f"❌ Nenhum plantio encontrado para o pivô {numero}."
    else:
        resposta = "Envie no formato: pivô 21, pivô 36, etc."

    await update.message.reply_text(resposta, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🤖 Bot rodando...")
    app.run_polling()

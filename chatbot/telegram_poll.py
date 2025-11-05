# chatbot/telegram_poll.py
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os, json, re, requests
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DJANGO_LINK_URL = os.getenv("DJANGO_LINK_URL")
DJANGO_WEBHOOK_URL = os.getenv("DJANGO_WEBHOOK_URL")

E164_RX = re.compile(r'^\+\d{8,15}$')
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "+55")  # fallback para normalizar

# ------ Funções auxiliares ------

def normalize_phone(raw: str) -> str:
    # remove tudo que não é dígito
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        return ""
    # se já vier com country code (11-15 dígitos tipicamente), prefixa "+"
    if raw.startswith("+") or len(digits) >= 11:
        return f"+{digits}"
    # fallback: assume país default (ex. Brasil)
    return f"{DEFAULT_COUNTRY}{digits}"

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} causou o erro {context.error}')

# ------ Funções de First Login ------

def share_contact_keyboard():
    kb = [[KeyboardButton(text="Compartilhar contato", request_contact=True)]]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Olá, {user.mention_html()}!\nToque no botão abaixo para compartilhar seu telefone cadastrado.",
        reply_markup=share_contact_keyboard()
    )

# ------ Atualização de Contato no DB ------

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extrai telefone e chat_id
    msg = update.message
    chat_id = str(msg.chat.id)
    c = msg.contact
    if not c:
        return
    raw_phone = c.phone_number or ""
    phone = normalize_phone(raw_phone)

    # manda para o Django vincular chat_id -> paciente
    try:
        r = requests.post(DJANGO_LINK_URL, json={"chat_id": chat_id, "phone": phone}, timeout=10)
        ok = (r.status_code // 100 == 2)
    except Exception as e:
        ok = False
        print("link error:", e)

    if ok:
        await msg.reply_text("Contato vinculado. Você já pode enviar suas respostas por aqui.")
    else:
        await msg.reply_text("Não encontrei seu número no cadastro. Fale com a equipe.")

# ------ Respostas do Usuário (Texto) ------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    chat_id = str(msg.chat.id)
    text = (msg.text or "").strip()

    # payload genérico para enviar para o webhook do Django
    generic = {
        "results": [
            {
                "from": f"{chat_id}",
                "message": {"text": text}
            }
        ]
    }
    try:
        requests.post(DJANGO_WEBHOOK_URL, json=generic, timeout=10)
    except Exception as e:
        print("webhook post error:", e)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))  # contato
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # texto
    app.add_error_handler(error_handler)
    print("Bot (polling) rodando... Ctrl+C para parar.")
    app.run_polling(poll_interval=5.0, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

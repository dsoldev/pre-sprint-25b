# pre-sprint-25b

## Setup Telegram Bot
1. Crie um novo bot no Telegram conversando com [@BotFather](https://telegram.me/BotFather).
2. Use o comando `/newbot` e siga as instruções para configurar seu bot.
3. Copie o token do bot fornecido pelo BotFather.

## Setup .env File
Crie um arquivo `.env` no diretório raiz do projeto com o seguinte conteúdo:
```
# Configuration
DJANGO_LINK_URL = http://127.0.0.1:8000/api/telegram/link/
DJANGO_WEBHOOK_URL = http://127.0.0.1:8000/webhook/
DEFAULT_COUNTRY = +55

# Django Settings
DJANGO_DEBUG = True

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = ...your-telegram-bot-token...
```

### Instalando Dependências
Todas as de Django e também:
```
pip install "python-telegram-bot==20.*"
pip install requests
```

### Fazendo Migrações
```
python manage.py makemigrations
python manage.py migrate
```

### Criando Superusuário
```
python manage.py createsuperuser
```

### Rodando o Servidor
Em um terminal, execute:
```
python manage.py runserver
```
em outro terminal, execute:
```
python -m chatbot.telegram_poll
```
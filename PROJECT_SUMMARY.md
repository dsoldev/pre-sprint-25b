# Visão geral
Plataforma Django para acompanhamento de pacientes que envia roteiros de perguntas diárias e captura respostas via Telegram. O projeto expõe um painel web para operadores acompanharem pacientes e utiliza um bot para vincular contatos e encaminhar respostas ao backend.

## Estrutura de dados
- **Questions** guarda o texto das perguntas.
- **Scripts** define títulos, descrições e a sequência JSON de perguntas por dia.
- **Patients** referencia um script, armazena idade, telefone e o `telegram_chat_id` vinculado.
- **Answers** registra conteúdo respondido por paciente e dia, com carimbo de criação.

## Funcionalidades principais
- **Painel de controle** (`/controlpanel/`): lista pacientes, mostra respostas por dia e permite disparar a próxima pergunta do roteiro calculando o próximo dia livre.
- **Linkagem Telegram** (`/api/telegram/link/`): recebe `chat_id` e telefone, associa ao paciente correspondente e salva o identificador do chat.
- **Envio de pergunta** (`/send_question/`): busca a próxima pergunta na sequência do script, envia via Telegram se o paciente já estiver vinculado e cria um registro `Answers` com status `AGUARDANDO`.
- **Webhook de respostas** (`/webhook/`): recebe mensagens do bot e preenche o conteúdo pendente mais recente para aquele paciente.
- **Bot Telegram (`python -m chatbot.telegram_poll`)**: orienta o usuário a compartilhar contato, chama o endpoint de linkagem e encaminha textos ao webhook.
- **Worker 17h** (`python manage.py worker_17h`): esboço de comando para agendar e reenviar perguntas após 17h, ainda a ser implementado.

## Interface web
Template `control_panel.html` usa um seletor de paciente, tabela de respostas e botão para enviar a próxima pergunta, estilizados com `static/chatbot/styles.css`.

## Configuração
Variáveis `.env` exigidas incluem URLs do webhook e token do bot. Dependências principais: Django, python-telegram-bot 20.x e requests. Migrações padrão e criação de superusuário seguem o fluxo Django habitual; execução envolve `python manage.py runserver` em paralelo ao bot em `python -m chatbot.telegram_poll`.
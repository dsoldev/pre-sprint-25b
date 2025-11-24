# chatbot/management/commands/worker_17h.py
import os
import time
from datetime import timedelta

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from chatbot.models import Patients  # <<< use o seu model aqui


class Command(BaseCommand):
    help = "Loop simples que verifica mensagens e envia se já passou 17h"

    def handle(self, *args, **options):
        token = os.getenv("TELEGRAM_BOT_TOKEN")

        base_url = f"https://api.telegram.org/bot{token}/sendMessage"

        self.stdout.write("Iniciando worker de mensagens 17h...")

        while True:
            now = timezone.now()
            cutoff = now - timedelta(hours=17)

			
            # 1. Verificar mensagens pendentes: Pacientees que 
                # 1.1 Já passou 17h desda ultima mensagem enviada
                # 1.2 Não chegou no fim do roteiro
            # 2. Se existerem mensagens pendentes, enviar via Telegram API - marcar no db a data de envio e que esta esperando resposta
                # 2.1 Pode tratar diferente se a ultima mensagem ainda estiver esperando resposta
                # 2.2 Pode
            # Aguardar TEMPO (1minuto) e repetir
            pendentes = []
            print(f"mandei, horario: {now}, cutoff: {cutoff}, pendentes: {len(pendentes)}")
            for msg in pendentes:
                pass

            # espera antes de checar de novo (ex.: 60s)
            time.sleep(60)

# Execução (novo terminal):
# python manage.py worker_17h
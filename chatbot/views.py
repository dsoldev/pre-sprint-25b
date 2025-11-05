# views.py
import json
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.urls import reverse
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
import requests

from .models import Patients, Answers, Scripts, Questions

def control_panel(request):
    patients = Patients.objects.all().order_by('name')

    # Paciente selecionado
    selected_name = request.GET['patient']
    selected_patient = patients.filter(name=selected_name).first() if selected_name else None

    # Linhas da tabela
    rows = []
    next_day = None
    if selected_patient:
        answers_qs = (
            Answers.objects
            .select_related('patient', 'question')
            .filter(patient=selected_patient)
            .order_by('day_number')
        )
        for a in answers_qs:
            rows.append({
                'day_number': a.day_number,
                'question': a.question.content,
                'content': a.content,
                'answered_on': localtime(a.answered_on).strftime('%Y-%m-%d %H:%M:%S'),
            })
        # Pega o valor do próximo dia
        next_day = (rows[-1]['day_number'] + 1) if rows else 1

    context = {
        'patients': patients,
        'selected_name': selected_name,
        'rows': rows,
        'next_day': next_day,
        'send_api_url': reverse('send_question'),  # nomeado em urls.py
    }
    return render(request, 'chatbot/control_panel.html', context)

# ------ Rota de Vinculação TelegramID e Número de Telefone ------

@csrf_exempt
def telegram_link(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    chat_id = str(data['chat_id'])
    phone = str(data['phone'])
    if not chat_id or not phone:
        return HttpResponseBadRequest('Missing fields')

    p = Patients.objects.filter(cellphone=phone).first()
    if not p:  # não achou paciente
        return JsonResponse({"ok": False, "error": "not_found"}, status=404)

    if p.telegram_chat_id != chat_id:  # numero no db, atualiza telegram_chat_id
        p.telegram_chat_id = chat_id
        p.save(update_fields=['telegram_chat_id'])

    return JsonResponse({"ok": True})

# ------ Rota de Envio de Pergunta ------

def send_telegram_message(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN  # defina no settings.py (ou via env e carregue lá)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": str(chat_id), "text": text}
    try:
        requests.post(url, json=payload, timeout=10).raise_for_status()
    except requests.RequestException as e:
        # logue se quiser
        print(f"[telegram] erro ao enviar: {e}")

def send_question(request):
    """
    POST form-data: patient_name
    Comportamento: calcula a próxima pergunta do script e responde apenas "OK".
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    patient_name = request.POST['patient_name']
    # get script_id from patient
    patient = Patients.objects.filter(name=patient_name).first()
    scripts = Scripts.objects.all().filter(id=patient.script.id)
    question_sequence = scripts[0].questions_sequence
    last = Answers.objects.filter(patient=patient).aggregate(m=Max('day_number'))['m']

    next_day = last + 1 if last else 1
    question_id = question_sequence[str(next_day)]
    question = Questions.objects.filter(id=question_id).first()

    print(patient, question.content)

    # Aqui você integraria com o sistema de envio de mensagens (SMS, WhatsApp, etc.)
    print(f"Enviando pergunta para {patient.name}: {question.content}")
    # Simulação de envio...
    if patient.telegram_chat_id:
        send_telegram_message(patient.telegram_chat_id, question.content)
        # Vamos deixar a resposta no DB como "AGUARDANDO" até o usuário responder
        Answers.objects.create(
            question=question,
            patient=patient,
            day_number=next_day,
            content='AGUARDANDO'
        )
    else:
        print(f"Paciente {patient.name} não tem telegram_chat_id vinculado.")
    # redirecionar de volta ao painel de controle com paciente selecionado
    return redirect(f"{reverse('control_panel')}?patient={patient.name}")

# ------ Webhook Para Receber Respostas ------

@csrf_exempt
def webhook(request):
    data = json.loads(request.body.decode('utf-8'))

    results = data['results']

    item = results[0]
    sender = item['from']
    print("Recebido de:", sender)
    text = item['message']['text'].strip()

    # get patient by telegram_chat_id
    patient = Patients.objects.filter(telegram_chat_id=sender).first()

    # get last answer waiting for this patient
    last_answer = Answers.objects.filter(patient=patient, content='AGUARDANDO').order_by('-day_number').first()
    if last_answer:
        last_answer.content = text
        last_answer.save(update_fields=['content'])
        print(f"Resposta do paciente {patient.name} registrada: {text}")
    else:
        print(f"Não estamos aguardando nenhuma resposta do paciente {patient.name}.")

    return HttpResponse("OK")
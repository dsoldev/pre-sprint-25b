# views.py
import json
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.timezone import localtime
from django.urls import reverse
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt

from .models import Patients, Answers, Scripts, Questions

def control_panel(request):
    patients = Patients.objects.all().order_by('name')

    # Paciente selecionado (via GET ?patient=Nome); opcionalmente selecione o 1º por padrão
    selected_name = request.GET.get('patient', '')
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


def send_question(request):
    """
    POST form-data: patient_name
    Comportamento: calcula a próxima pergunta do script e responde apenas "OK".
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    patient_name = request.POST.get('patient_name')
    # get script_id from patient
    patient = Patients.objects.filter(name=patient_name).first()
    scripts = Scripts.objects.all().filter(id=patient.script.id)
    question_sequence = scripts[0].questions_sequence
    last = Answers.objects.filter(patient=patient).aggregate(m=Max('day_number'))['m']

    next_day = last + 1 if last else 1
    question_id = question_sequence.get(str(next_day))
    question = Questions.objects.filter(id=question_id).first()

    print(patient, question.content)

    # Aqui você integraria com o sistema de envio de mensagens (SMS, WhatsApp, etc.)
    print(f"Enviando pergunta para {patient.name}: {question.content}")
    # Simulação de envio...
    # Salvar resposta OK para teste
    Answers.objects.create(
        question=question,
        patient=patient,
        day_number=next_day,
        content='OK'
    )
    # redirecionar de volta ao painel de controle com paciente selecionado
    return redirect(f"{reverse('control_panel')}?patient={patient.name}")

@csrf_exempt
def webhook(request):
    from_number = request.POST.get('From', '')  # ex: 'whatsapp:+5511999998888'
    body = request.POST.get('Body', '').strip()

    # Aqui você processaria a mensagem recebida
    print(f"Mensagem recebida de {from_number}: {body}")

    # Responder com uma mensagem de confirmação
    return HttpResponse("OK")
import json
from django.shortcuts import render
from django.utils.timezone import localtime
from django.utils.safestring import mark_safe
from .models import Questions, Scripts, Patients, Answers

def control_panel(request):
    questions = Questions.objects.all()
    scripts = Scripts.objects.all()
    patients = Patients.objects.all()
    answers = Answers.objects.all()

    # Montar dicionário de respostas por paciente
    answers_by_patient = {}
    for p in patients:
        answers_by_patient[p.name] = {}
    
    # Preencher o dicionário com as respostas
    for a in answers:
        answers_by_patient[a.patient.name][a.day_number] = {
            'question': a.question.content,
            'content': a.content,
            'answered_on': localtime(a.answered_on).strftime('%Y-%m-%d %H:%M:%S')
        }
    

    return render(
        request,
        "chatbot/control_panel.html",
        {
            "patients": patients,
            "answers_by_patient_json": mark_safe(json.dumps(answers_by_patient)),
        },
    )
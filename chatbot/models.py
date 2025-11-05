from django.db import models

class Questions(models.Model):
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.content[:50]}"

class Scripts(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    questions_sequence = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Patients(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    script = models.ForeignKey(Scripts, on_delete=models.CASCADE) # https://docs.djangoproject.com/en/5.2/topics/db/examples/many_to_one/
    cellphone = models.CharField(max_length=15)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    content = models.TextField()
    answered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.day_number}"



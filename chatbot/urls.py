from django.urls import include, path
from . import views

urlpatterns = [
    path('controlpanel/', views.control_panel, name='control_panel'),
    path('send_question/', views.send_question, name='send_question'),
    path('webhook/', views.webhook, name='webhook'),
    path('api/telegram/link/', views.telegram_link, name='telegram_link'),
]

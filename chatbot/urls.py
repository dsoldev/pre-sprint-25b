from django.urls import include, path
from . import views

urlpatterns = [
    path('controlpanel/', views.control_panel, name='control_panel')
]

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path("chat/", views.chat, name="chat"),
    path("history/", views.chat_history, name="chat_history"),
    path('chat/clear/', views.clear_history, name='clear_history'),

]
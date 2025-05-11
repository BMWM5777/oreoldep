from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .utils import get_bot_response
from django.shortcuts import render
import logging
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

def chat(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse({"history": []})
        msgs = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
        history = []
        for m in msgs:
            history.append({
                "from": "user",
                "text": m.message,
                "timestamp": m.timestamp.isoformat()
            })
            history.append({
                "from": "bot",
                "text": m.response,
                "timestamp": m.timestamp.isoformat()
            })
        return JsonResponse({"history": history})

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({
                "response": "Пожалуйста, авторизуйтесь, чтобы обратиться к консультанту."
            })
        
        user_input = request.POST.get("message")
        if not user_input:
            return JsonResponse({"error": "Пустой запрос"}, status=400)

        try:
            bot_response = get_bot_response(user_input)
            ChatMessage.objects.create(
                user=request.user,
                message=user_input,
                response=bot_response
            )
            return JsonResponse({"response": bot_response})
        except Exception:
            logger.exception("Ошибка в обработке чата")
            return JsonResponse({"error": "Внутренняя ошибка сервера"}, status=500)

    return JsonResponse({"error": "Неподдерживаемый метод"}, status=405)

@login_required
def chat_history(request):
    """
    Возвращает весь диалог пользователя в формате JSON:
    [{'sender': 'user'|'bot', 'text': '...'}, ...]
    """
    qs = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    history = []
    for msg in qs:
        history.append({'sender': 'user', 'text': msg.message})
        history.append({'sender': 'bot',  'text': msg.response})
    return JsonResponse({'history': history})

@login_required
def clear_history(request):
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

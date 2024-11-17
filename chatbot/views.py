from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatSession
from .services import ChatbotService

# Create your views here.

@login_required
def chat_view(request):
    # Get or create a chat session for the user
    chat_session, created = ChatSession.objects.get_or_create(
        user=request.user,
        defaults={'user': request.user}
    )
    
    return render(request, 'chatbot/chat.html', {
        'chat_session': chat_session
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        chat_session = ChatSession.objects.get(user=request.user)
        
        chatbot = ChatbotService()
        response = chatbot.get_chat_response(chat_session, message)
        
        return JsonResponse({
            'message': response
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

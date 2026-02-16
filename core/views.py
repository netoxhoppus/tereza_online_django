from django.shortcuts import render
from django.http import JsonResponse
from .services.rag_service import TerezaAgent

from .services.memory import MemoryService

def chat_view(request):
    # Ensure session exists to use as session_id
    if not request.session.session_key:
        request.session.create()
    
    session_id = request.session.session_key
    response_text = None

    if request.method == 'POST':
        user_message = request.POST.get('message')
        if not user_message and request.content_type == 'application/json':
             import json
             try:
                 data = json.loads(request.body)
                 user_message = data.get('message')
             except:
                 pass

        if user_message:
            agent = TerezaAgent()
            response_text = agent.process_message(session_id, user_message)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.accepts('application/json'):
                 return JsonResponse({'response': response_text})

    # Fetch history for GET requests (and non-AJAX POSTs)
    memory_service = MemoryService()
    history = memory_service.get_history(session_id)

    return render(request, 'core/chat.html', {'response': response_text, 'history': history})

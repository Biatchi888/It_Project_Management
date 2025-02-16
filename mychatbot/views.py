from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_logic import convert_measurement, conversation_history

def chatbot_interface(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        result = convert_measurement(query)

        conversation_history.append(f'User: {query}')
        conversation_history.append(f'Chatbot: {result}')
        
        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'conversation_history': conversation_history})

    # Render only the chatbot (not the full page) for including in the parent template
    return render(request, 'mychatbot/mychatbot.html', {'conversation_history': conversation_history})

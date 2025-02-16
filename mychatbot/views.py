from django.shortcuts import render
from .chatbot_logic import convert_measurement, conversation_history


def chatbot_interface(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        result = convert_measurement(query)
        
        conversation_history.append(f'User: {query}')
        conversation_history.append(f'Chatbot: {result}')
        return render(request, 'mychatbot/mychatbot.html', {'conversation_history': conversation_history})

    return render(request, 'mychatbot/mychatbot.html', {'conversation_history': conversation_history})

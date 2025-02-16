from django.urls import path
from . import views


urlpatterns = [
    # path('mychatbot/', views.chatbot_interface, name='mychatbot'),
    path('', views.chatbot_interface, name='mychatbot'),

]

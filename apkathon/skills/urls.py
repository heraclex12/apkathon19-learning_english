from django.urls import path

from skills.views import writing, index, check_grammar

urlpatterns = [
    path('writing/', writing),
    path('', index),
    # path('listening/', views.listening, name='listening'),
    # path('speaking/', views.speaking, name='speaking'),
    # path('reading/', views.reading, name='reading'),
]
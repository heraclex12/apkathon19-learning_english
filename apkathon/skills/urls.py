from django.urls import path

from skills.views import writing, index, about, home_writing

urlpatterns = [
    path('writing/<int:article_id>/', writing),
    path('writing/', home_writing),
    path('', index),
    path('about/', about)
    # path('listening/', views.listening, name='listening'),
    # path('speaking/', views.speaking, name='speaking'),
    # path('reading/', views.reading, name='reading'),
]
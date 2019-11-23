from django.urls import path

from skills.views import writing, index, about, home_writing, listening, speaking, reading, home_speaking

urlpatterns = [
    path('writing/<int:article_id>/', writing),
    path('writing/', home_writing),
    path('', index),
    path('about/', about),
    path('listening/', listening, name='listening'),
    path('speaking/<int:article_id>/', speaking, name='speaking'),
    path('speaking/', home_speaking),
    path('reading/<int:article_id>/', reading, name='reading'),
]
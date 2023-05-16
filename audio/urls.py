from django.urls import path
from .views import AudioConvertView, AudioCreateView


urlpatterns = [
    path('audio/create/', AudioCreateView.as_view(), name='audio_create'),
    path('audio/<int:pk>/convert/', AudioConvertView.as_view(), name='audio_convert')
]

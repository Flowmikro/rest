import os
import subprocess
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from .models import Audio
from .serializers import AudioSerializer
from django.shortcuts import render, redirect
from .forms import AudioForm


class AudioConvertView(generics.RetrieveAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        wav_path = instance.wav_file.path
        mp3_path = os.path.splitext(wav_path)[0] + '.mp3'
        subprocess.call(['ffmpeg', '-i', wav_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', mp3_path])
        instance.mp3_file = os.path.relpath(mp3_path, settings.MEDIA_ROOT)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AudioCreateView(generics.CreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


def audio_create(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('audio_list')
        else:
            form = AudioForm()
        return render(request, 'audio_create.html', {'form': form})


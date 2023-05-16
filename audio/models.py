from django.db import models

from django.core.exceptions import ValidationError


def validate_wav(value):
    if not value.name.endswith('.wav'):
        raise ValidationError('Разрешены только файлы WAV.')


class Audio(models.Model):
    title = models.CharField(max_length=100)
    wav_file = models.FileField(upload_to='audio/', validators=[validate_wav])



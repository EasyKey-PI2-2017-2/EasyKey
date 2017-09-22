from django.db import models
from django.contrib.auth.models import User


def foto_upload_path(instance, filename):
    return texto_upload_path(instance, filename, subpath='')


class Chave(models.Model):
    TAMANHO_CHAVE = (('P', 'Pequena'),
                     ('M', 'Média'),
                     ('G', 'Grande'))
    usuario = models.ForeignKey(User)
    tamanho = models.CharField(
        max_length=1, verbose_name='Tamanho', choices=TAMANHO_CHAVE)
    timestamp = models.DateTimeField()
    imagem = models.ImageField(upload_to=foto_upload_path,
        verbose_name='Fotografia')

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

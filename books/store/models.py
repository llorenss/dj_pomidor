from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    author_name = models.CharField(max_length=255, verbose_name="Автор")
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

    
    class Meta:
        verbose_name='Книги'
        verbose_name_plural='Книги'
        # знак минус обратная сортировка
        # сортировка перейдёт в выдачу в браузер
        # ordering = ['-name']

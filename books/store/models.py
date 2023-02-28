from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    
    class Meta:
        verbose_name='Книги'
        verbose_name_plural='Книги'
        # знак минус обратная сортировка
        # сортировка перейдёт в выдачу в браузер
        ordering = ['-name']

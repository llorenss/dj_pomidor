from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    author_name = models.CharField(max_length=255, verbose_name="Автор")
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    readers = models.ManyToManyField(User, through='UserBookRelation')

    
    class Meta:
        verbose_name='Книги'
        verbose_name_plural='Книги'
        # знак минус обратная сортировка
        # сортировка перейдёт в выдачу в браузер
        # ordering = ['-name']

class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1,'a'),
        (2,'b'),
        (3,'c'),
        (4,'d'),
        (5,'e')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveBigIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'{self.user.username}:{self.book.name}, RATE {self.rate}'


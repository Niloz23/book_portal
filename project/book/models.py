from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Book(models.Model):
    class CategoryType(models.TextChoices):
        CATEGORY1 = '1', 'Фантастика'
        CATEGORY2 = '2', 'Детективы'
        CATEGORY3 = '3', 'Исторические'
        CATEGORY4 = '4', 'Научная литература'
        CATEGORY5 = '5', 'Классика'
        CATEGORY6 = '6', 'Древние рукописи'
        CATEGORY7 = '7', 'Биографии'
        CATEGORY8 = '8', 'Автографы авторов'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CategoryType.choices, null=False)
    descript = models.CharField(verbose_name='Текст',max_length = 250)
    year = models.CharField(max_length=4)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def get_author(self):
        author = self.user
        return author

    def __str__(self):
        return f'{self.header}'


    def get_absolute_url(self):
        x = 'books_detail'
        return reverse(x, args=[str(self.id)])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='Books', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(null=False, default=False)
    is_acept = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f'{self.comment_text[:20]}'

    def get_absolute_url(self):
        x = 'books_detail'
        return reverse(x, args=[str(self.id)])

class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.code

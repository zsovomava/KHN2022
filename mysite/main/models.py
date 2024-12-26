from random import choice

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Szerző', on_delete=models.CASCADE)
    title = models.CharField('Cím', max_length=300)
    topic = models.ForeignKey(
        Topic, verbose_name='Téma', on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField('Tartalom')
    pub_date = models.DateTimeField('Közzétételi dátum', default=timezone.now)

    class Meta:
        ordering = ['-pub_date', 'author']

    def __str__(self):
        return self.title + ' - #' + str(self.id)

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Szerző', on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(
        Post, verbose_name='Poszt', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Tartalom')
    pub_date = models.DateTimeField('Közzétételi dátum', default=timezone.now)

    class Meta:
        ordering = ['-pub_date', 'author']

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.post.pk}) + '#comment-' + str(self.pk)


class Tip(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:25]

    @staticmethod
    def get_a_tip():
        DEFAULT_TIPS = ['Legyen mindig nyitott, akárcsak a forráskódja!',
                        'Szabad ország, szabad szoftver!', 'Az élet szép.']
        tip = Tip.objects.order_by('?').first()
        if tip:
            tip = tip.text
        else:
            tip = choice(DEFAULT_TIPS)
        return tip

from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Felhasználó', on_delete=models.CASCADE)
    image = models.ImageField('Profilkép', default='default.png', upload_to='profile_pics')
    bio = models.TextField('Leírás', max_length=500, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return str(self.user)

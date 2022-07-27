from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null = True, upload_to = 'images/profile')
    pic_url = models.CharField(null = True, max_length=250)
    
    def get_absolute_url(self):
        return reverse('edit_profile')
    
    
    def __str__(self):
        return f'{self.user.username}: {self.user.first_name} {self.user.last_name}'
    
class ProfilePic(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Photo url for {self.user_id} @ {self.url}'
    
SPIRITS = (
    ('Candlemaker', 'Pointing-Candlemaker'),
    ('Stargazer', 'Ushering-Stargazer'),
    ('Voyager', 'Rejecting-Voyager'),
    ('Charmer', 'Butterfly-Charmer'),
    ('Bellmaker', 'Waving-Bellmaker'),    
)

class Spirit(models.Model):
    name = models.CharField(max_length=200)
    realm = models.CharField(max_length=100)
    url = models.CharField(max_length=200)    
    
    def __str__(self):
        return f'{self.id}: {self.name}'
        

class UserSpirit(models.Model):
    name = models.CharField(max_length=200)
    realm = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    user = models.ManyToManyField(User)
    user = models.ManyToManyField(User)
    

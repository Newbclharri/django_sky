from distutils.command.upload import upload
from distutils.text_file import TextFile
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
    ('Candlemaker', 'Candlemaker'),
    ('Stargazer', 'Stargazer'),
    ('Voyager', 'Voyager'),
    ('Charmer', 'Charmer'),
    ('Bellmaker', 'Bellmaker'),    
)

class Spirit(models.Model):
    tag = models.CharField(null=True, max_length=15)
    name = models.CharField(max_length=100)
    realm = models.CharField(max_length=100)
    url = models.CharField(max_length=200)   
    
    def __str__(self):
        return f'{self.id} - {self.tag}'
    
    class Meta:
        ordering = ['name']
        

class UserSpirit(models.Model):
    tag = models.CharField(
        null=True,
        max_length=15,
        choices=SPIRITS,
        default=SPIRITS[0][0],
        )
    name = models.CharField(max_length=100)
    realm = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, max_length= 500)
    user = models.ManyToManyField(User)
    
    def __str__(self):
        return f'{self.id} - {self.tag}'

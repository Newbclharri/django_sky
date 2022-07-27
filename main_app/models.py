from django.db import models
from ckeditor.fields import RichTextField
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
    tag = models.CharField(null=True, max_length=20)
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
        max_length=20,
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
    
    def get_absolute_url(self):
        return reverse('spirits_detail', kwargs={'pk': self.id})
    
REALMS = (
    ('Isle of Dawn', 'Isle'),
    ('Daylight Prairie', 'Daylight'),
    ('Hidden Forest', 'Forest'),
    ('Valley of Triump', 'Valley'),
    ('Golden Wasteland', 'Wasteland'),
    ('Vault of Knowledge', 'Vault'),
    ('Secret Area', 'Secret'),
)

class WingedLight(models.Model):
    realm = models.CharField(
        max_length=20,
        choices=REALMS,
        default=REALMS[0][0]
        )
    location = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} - {self.realm}'
    
    class Meta:
            ordering = ['realm']

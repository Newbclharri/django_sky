from distutils.log import error
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
import boto3, uuid
from .forms import SignUpForm, EditProfileForm
from.models import Profile, ProfilePic, User

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'sky-cotl-cj'


# Create your views here.

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # request.method == 'GET'
    form = SignUpForm()
    context = {'form': form, 'error_message': error_message}            
    return render(request, 'registration/signup.html', context)

class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = 'home'
    
    def get_object(self):
        return self.request.user
    
def add_profilepic(request):
    photo_file = request.FILES.get('photo-file', None)
    print('user id: ',request.user.id, photo_file)
    if photo_file:
        session = boto3.Session(profile_name='sky')
        s3_client = session.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3_client.upload_fileobj(photo_file, BUCKET, key)
            # build full url string
            user_profile = Profile(user = request.user)
            url  = f'{S3_BASE_URL}{BUCKET}/{key}'
            user_profile.pic_url = url
            user_profile.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('edit_profile')

def home(request):
    return render(request, 'home.html')
from ast import Del
from hashlib import new
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import boto3, uuid
from .forms import SignUpForm, EditProfileForm, SpiritForm
from.models import Profile, ProfilePic, Spirit, UserSpirit, User, WingedLight
from django.urls import reverse_lazy, reverse
import psycopg2

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'sky-cotl-cj'


# Create your views here.
def home(request):
    return render(request, 'home.html')

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

class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    
    def get_object(self):
        return self.request.user
    
    success_url = reverse_lazy('edit_profile')
    
@login_required 
def add_profilepic(request):
    # check to see if there is an instance of the model Profile
    # if not save an instance of profile linked to the active user making the request        
    if not(Profile.objects.filter(user = request.user).exists()):
            Profile(user = request.user).save()
    print(request.user.profile)
    
    # add file to s3 bucket with authentic url
    photo_file = request.FILES.get('photo-file', None)
    print('user id: ',request.user.id, photo_file)
    if photo_file:
        session = boto3.Session(profile_name='sky')
        s3_client = session.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]        
        s3_client.upload_fileobj(photo_file, BUCKET, key)
        # build full url string
        user_profile = Profile(user = request.user)
        url  = f'{S3_BASE_URL}{BUCKET}/{key}'
        
        
        connection = psycopg2.connect(  user="contactharrisc2",
                                        password="J0s3aRr901",
                                        host="localhost",
                                        port="5432",
                                        database="sky_cotl")
        cursor = connection.cursor()
        print("Table Before updating record: ")
        sql_select_query = """select * from main_app_profile where user_id = %s"""
        cursor.execute(sql_select_query, (request.user.id,))
        record = cursor.fetchone()
        print(record)
        
        #Update single record now
        sql_update_query = """Update main_app_profile set pic_url = %s where user_id = %s"""
        cursor.execute(sql_update_query, (url, request.user.id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully")
        
        print("Table After updating record ")
        sql_select_query = """select * from main_app_profile where user_id = %s"""
        cursor.execute(sql_select_query, (request.user.id,))
        record = cursor.fetchone()
        print(record)
        
        # closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect('edit_profile')


@login_required
def add_screenshot(request):
    spirit_data = ""
    blank_form = SpiritForm()
    form = SpiritForm(request.POST)
    if form.is_valid():
        new_spirit = form.save(commit=False)
        spirit_data = Spirit.objects.filter(name = new_spirit.name)
        new_spirit.user_id = request.user_id
        new_spirit.realm = spirit_data.realm
        new_spirit.url = spirit_data.url
    return render(request, "add_spirit.html", {
        'spirit_form': blank_form,
    })

class SpiritCreate(LoginRequiredMixin, CreateView):
    model = UserSpirit
    fields = ['tag', 'description']
    def form_valid(self, form):
        user_spirit = form.instance
        # user_spirit = self.object
        # user_spirit= form.save(commit=False)
        user_spirit.save()
        user_spirit.user.add(self.request.user)
        data_spirit = Spirit.objects.get(tag=user_spirit.tag)
        user_spirit.name = data_spirit.name
        user_spirit.realm = data_spirit.realm
        user_spirit.url = data_spirit.url
        user_spirit.save()
                
        # user_spirit = Spirit.objects.get(user = self.request.user)
        # data_spirit = Spirit.objects.get(tag = user_spirit.tag)
        # user_spirit.name = data_spirit.name
        # user_spirit.realm = data_spirit.realm
        # user_spirit.url = data_spirit.url
        # user_spirit.set()
        return super().form_valid(form)

class SpiritList(LoginRequiredMixin, ListView):
    model = UserSpirit 

class SpiritDetail(LoginRequiredMixin, DetailView):
    model = UserSpirit
    success_url = reverse_lazy('/spirits/')
    
class SpiritUpdate(LoginRequiredMixin, UpdateView):
    model = UserSpirit
    fields = ['description']
    
class SpiritDelete(LoginRequiredMixin, DeleteView):
    model = UserSpirit
    success_url = reverse_lazy('spirits_index')
    
class WingedLightList(LoginRequiredMixin, ListView):
    model = WingedLight

class WingedLightDetail(LoginRequiredMixin, DetailView):
    model = WingedLight
    success_url = '/wingedlight/'
    
class WingedLightCreate(LoginRequiredMixin, CreateView):
    model = WingedLight
    fields= ['wingedlight', 'realm', 'location']
    
    def form_valid(self, form):
        new_wingedlight = form.instance
        new_wingedlight.user_id = self.request.user.pk
        new_wingedlight.save()
        photo_file = self.request.FILES.get('photo-file', None)
        
        if photo_file:
            session = boto3.Session(profile_name='sky')
            s3_client = session.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]        
            s3_client.upload_fileobj(photo_file, BUCKET, key)
            # build full url string
            url  = f'{S3_BASE_URL}{BUCKET}/{key}'
            new_wingedlight.url = url
        return super().form_valid(form) 
    success_url = '/wingedlight/'
    

class WingedLightUpdate(LoginRequiredMixin, UpdateView):
    model = WingedLight
    fields = ['realm', 'location']

class WingedLightDelete(LoginRequiredMixin, DeleteView):
    model = WingedLight
    success_url = '/wingedlight/'

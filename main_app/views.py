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
from django.urls import reverse_lazy
import psycopg2

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
    
    def get_object(self):
        return self.request.user
    
    success_url = reverse_lazy('edit_profile')
    
def add_profilepic(request):
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

def home(request):
    return render(request, 'home.html')
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/edit_profile/', views.UserEditView.as_view(), name = 'edit_profile'),
    path('accounts/add_profilepic/', views.add_profilepic, name='add_profilepic'),
]
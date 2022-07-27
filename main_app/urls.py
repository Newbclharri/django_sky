from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/edit_profile/', views.UserEditView.as_view(), name = 'edit_profile'),
    path('accounts/add_profilepic/', views.add_profilepic, name='add_profilepic'),
    path('spirits/', views.SpiritList.as_view(), name='toys_index'),
    #path('spirits/<int:pk>/', views.SpiritDetail.as_view(), name='spirits_detail'),
    path('spirits/add_spirit/', views.add_spirit, name='add_spirit'),
    path('spirits/create/',views.SpiritCreate.as_view(), name='spirits_create')
]
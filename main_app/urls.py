from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/edit_profile/', views.UserEditView.as_view(), name = 'edit_profile'),
    path('accounts/add_profilepic/', views.add_profilepic, name='add_profilepic'),
    path('spirits/', views.SpiritList.as_view(), name='spirits_index'),
    path('spirits/create/',views.SpiritCreate.as_view(), name='spirits_create'),
    path('spirits/<int:pk>/', views.SpiritDetail.as_view(), name='spirits_detail'),
    path('spirits/<int:pk>/update/', views.SpiritUpdate.as_view(), name='spirits_update'),
    path('spirits/<int:pk>/delete/', views.SpiritDelete.as_view(), name='spirits_delete'),
    path('wingedlight/', views.WingedLightList.as_view(), name='wingedlight_index'),
    path('wingedlight/<int:pk>/', views.WingedLightDetail.as_view(), name='wingedlight_detail'),
    path('wingedlight/create/', views.WingedLightCreate.as_view(), name='wingedlight_create'),
    path('wingedlight/<int:pk>/update/', views.WingedLightUpdate.as_view(), name='wingedlight_update'),
    path('wingedlight/<int:pk>/delete/', views.WingedLightDelete.as_view(), name='wingedlight_delete'),
]
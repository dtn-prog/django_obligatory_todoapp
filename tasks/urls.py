from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit_task/<str:id>', views.edit_task, name='edit_task'),
    path('delete_task/<str:id>',views.delete_task, name='delete_task'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout')
]

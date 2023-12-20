from django.contrib import admin
from django.urls import path
from .views import game, show, edit, update, destroy, upload_csv, display_rankings, register, user_login, user_logout, Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('game', game, name='game'),
    path('', show, name="show_results"),
    path('edit/<int:id>', edit, name='edit'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', destroy, name='destroy'),
    path('upload', upload_csv, name='upload_csv'),
    path('ranking_list', display_rankings, name="ranking_list"),
    path("home", Home.as_view(), name="home"),
    ]
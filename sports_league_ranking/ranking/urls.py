from django.contrib import admin
from django.urls import path
from .views import game, show, edit, update, destroy, upload_csv, display_rankings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('game', game),
    path('show', show),
    path('edit/<int:id>', edit),
    path('update/<int:id>', update),
    path('delete/<int:id>', destroy),
    path('upload', upload_csv, name='upload_csv'),
    path('ranking_list', display_rankings),
    ]
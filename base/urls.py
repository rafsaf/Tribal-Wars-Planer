from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.base_view, name='base'),
    path('planer/', views.OutlineList.as_view(), name='planer'),
    path('planer/update', views.database_update, name='planer_update'),
    path('planer/create/', views.new_outline_create, name='planer_create'),
    path('planer/create/<int:id>/select_tribe', views.new_outline_create_select, name='planer_create_select'),
    path('planer/<int:pk>/delete', views.OutlineDelete.as_view(), name='planer_delete'),
    path('documentation', views.base_documentation, name='documentation'),
    path('documentation/worlds', views.WorldList.as_view(), name='worlds'),


]

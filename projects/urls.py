from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list_view, name='project_list'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/complete/', views.complete_project, name='complete_project'),
    path('<int:project_id>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
]
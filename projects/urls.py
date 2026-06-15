from django.urls import path
from projects import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list_view, name='project_list'),
    path('<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('<int:project_id>/complete/', views.complete_project, name='complete_project'),
    path('<int:project_id>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('skills/', views.skill_autocomplete, name='skill_autocomplete'),
    path('<int:project_id>/skills/add/', views.add_project_skill, name='add_project_skill'),
    path('<int:project_id>/skills/<int:skill_id>/remove/', views.remove_project_skill, name='remove_project_skill'),
]
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.participants_list_view, name='participants_list'),
    path('<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('<int:user_id>/edit/', views.edit_profile_view, name='edit_profile'),
    path('<int:user_id>/change-password/', views.change_password_view, name='change_password'),
    path('change-password/', views.redirect_to_change_password, name='redirect_change_password'),
    path('edit-profile/', views.redirect_to_edit_profile, name='redirect_edit_profile'),
]

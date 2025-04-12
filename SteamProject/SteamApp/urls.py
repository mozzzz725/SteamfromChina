from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-account/', views.edit_user_view, name='edit_account'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('post-game/', views.post_game_view, name='post_game'),
    # path('my-games/', views.my_games_view, name='my_games'), # <- No need for this
    path('edit-game/<int:id>', views.edit_game_view, name='edit_game'),
    path('continue/<int:game_id>/', views.continue_warning, name='continue_warning'),
    path('delete/<int:id>/', views.delete_game, name='delete_game'),
]

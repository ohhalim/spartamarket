from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/follow/', views.follow_view, name='follow'),
    path('profile/<str:username>/products/', views.profile_products_view, name='profile_products'),
    path('profile/<str:username>/products/like/', views.profile_like_view, name='profile_like'),
]   
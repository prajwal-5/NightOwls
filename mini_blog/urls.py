from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('about', views.about, name="aboutpage"),
    path('contact', views.contact, name="contactpage"),
    path('dashboard', views.dashboard, name="dashboardpage"),
    path('signup', views.signup, name="signuppage"),
    path('login', views.user_login, name="loginpage"),
    path('logout', views.user_logout, name="logoutpage"),
    path('addpost', views.add_post, name="addpostpage"),
    path('updatepost/<int:id>', views.update_post, name="updatepostpage"),
    path('delete/<int:id>', views.delete_post, name="deletepostpage"),
]

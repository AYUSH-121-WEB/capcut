from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, ProfileView, ProfileEditView, follow_user
from .forms import LoginForm

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
]

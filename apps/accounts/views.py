from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignUpForm, ProfileUpdateForm
from .models import UserProfile

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(UserProfile, user__username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user = self.get_object().user
        # Check if currently logged in user is following the profile user
        # user.following.all() returns UserProfiles that 'user' is following.
        context['is_following'] = user.following.filter(user=profile_user).exists()
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'accounts/edit_profile.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

@require_POST
def follow_user(request, username):
    if not request.user.is_authenticated:
         return JsonResponse({'error': 'Login required'}, status=401)
    
    target_user = get_object_or_404(User, username=username)
    user_profile = target_user.profile
    
    if request.user == target_user:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

    if request.user in user_profile.followers.all():
        user_profile.followers.remove(request.user)
        is_following = False
    else:
        user_profile.followers.add(request.user)
        is_following = True
        
    return JsonResponse({
        'is_following': is_following,
        'follower_count': user_profile.followers.count()
    })

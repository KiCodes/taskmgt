
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, View
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect

# Create your views here.
class SignUpView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignUpForm
    success_url = 'login'

    def form_valid(self, form):
        # Create a new user with the data from the form
        user = form.save()
        
        # Check if the group exists, create it if it doesn't
        group, created = Group.objects.get_or_create(name='Task Users')

        # Add the user to the group
        user.groups.add(group)

        if created:
            # Perform additional actions for newly created groups
            print("New group created:", group.name)
        return super().form_valid(form)
    
class LoginPageView(LoginView):
    template_name = 'auth/login.html'
    redirect_field_name = 'next'
    
    def get_success_url(self):
        # Get the URL to redirect to from the 'next' parameter in the request
        redirect_to = self.request.GET.get(self.redirect_field_name)
        
        # Check if the URL is safe to redirect to (prevent open redirects)
        if redirect_to and url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=None):
            return redirect_to
        
        # If 'next' parameter is not present or not safe, use a default URL
        return '/auth/profile'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/auth/index')
        return super().get(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # Log out the user
        logout(request)
        # Redirect to a specific URL after logout
        return redirect('login/') 
    
class ProfileView(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        # Get the current user
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user'] = user
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"login?next={request.path}")
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(PasswordChangeView):
    template_name = 'auth/change_password.html'
    success_url = reverse_lazy('profile')
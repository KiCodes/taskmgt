
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, View

from authentication.models import UserImage
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect, render

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
    # query field parameter conventionally names as 'next' for routing user to the page they tried to access
    # before they were rerouted to log in
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
        # prevent an authenticated user from seeing the login page and having to login in twice
        # redirect user to profile if they have logged in already
        if self.request.user.is_authenticated:
            return redirect('/auth/profile')
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
        # super().get_context_data ensures that you're extending the context data provided by the superclass. 
        # This is important because DetailView already provides some context data by default, like the object being displayed.
        # you're making sure that this default behavior is preserved while adding your custom context data 
        context = super().get_context_data(**kwargs)
        # passing the current user as object context to the template
        user = self.get_object()
        image = UserImage.objects.filter(user=user).last()
        context['user'] = user
        context['image'] = image
        return context
    
    # dispatch is called when Annonymous user tries to make a request on a page
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # rerouting to the login page and attaching a 'next' parameter query to the url with the value of the url user tried to access
            return redirect(f"login/?next={request.path}")
        return super().dispatch(request, *args, **kwargs)
        


class ChangePasswordView(PasswordChangeView):
    # inheriting PasswordChangeView allows us to simply replace the parent class template name and success url 
    # the form handling is done in the parent class 
    template_name = 'auth/change_password.html'
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # rerouting to the login page and attaching a 'next' parameter query to the url with the value of the url user tried to access
            return redirect(f"login?next={request.path}")
        return super().dispatch(request, *args, **kwargs)
    

from .forms import UserImageForm
class UploadImageView(View):
    def get(self, request, *args, **kwargs):
        form = UserImageForm()
        return render(request, 'auth/upload_image.html', {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect('profile')  # Redirect to profile page upon successful upload
        else:
            # If form is not valid, render the form again with errors
            return render(request, 'auth/upload_image.html', {'form': form})
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from userprofile.models import User
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from content.views import ContentView


def favicon(request):
	# View for serving the favicon
	return render(request, 'main/favicon.html')

def get_template(request):
	"""
	View for determining the appropriate template based on user authentication status
	If the user is authenticated, display the user's feed
	If the user is not authenticated, display the login/registration page
	
	"""
	if request.user.is_authenticated:
		return ContentView.as_view()(request)
	else:
		return UserLoginView.as_view()(request)


class UserRegisterView(CreateView):
	"""
	View for user registration, inherits from Django's CreateView
	
	"""
	model = User
	form_class = SignUpForm
	success_url = '/'
	template_name = 'main/register.html'

	def form_valid(self, form):
		# Override form_valid to log in the user upon successful registration
		response = super().form_valid(form)
		login(self.request, self.object)
		return response


class UserLoginView(LoginView):
	"""
	View for user login, inherits from Django's LoginView
	
	"""
	template_name = 'main/login.html'
	form_class = LoginForm

	def get_success_url(self):
		# Redirect to the home page upon successful login
		return reverse_lazy('main:home')


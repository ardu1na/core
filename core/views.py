
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView

class Logout(LogoutView):
    def get_success_url(self):
        return reverse_lazy('index')

class Login(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index') 
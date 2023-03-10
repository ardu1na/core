
from django.urls import reverse_lazy
from django.views.generic import View
from django.http import HttpResponseRedirect

class Login(View):
    template_name = '/admin/login/'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index') 

def logout(request):
    return HttpResponseRedirect('/admin/logout/')
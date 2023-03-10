from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from core import views
from core.views import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', login_required(views.logout), name='logout'),
    path('', include('inventory.urls'))
]

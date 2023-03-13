from django.contrib import admin
from django.urls import path, include

from core.views import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    
    path('', include('inventory.urls'))
]

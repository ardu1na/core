from django.urls import path
from django.contrib.auth.decorators import login_required
from inventory import views
urlpatterns = [
    
    
    path('', login_required(views.index), name='index'),
    path('items/', login_required(views.items), name='items'),
    path('deleteitem/<int:id>', views.deleteitem, name="deleteitem"),

    path('departments/', login_required(views.departments), name='departments'),

]

from django.urls import path
from django.contrib.auth.decorators import login_required
from inventory import views
urlpatterns = [
    
    
    path('', login_required(views.index), name='index'),
    path('items/', login_required(views.items), name='items'),
    path('items/<int:id>/', login_required(views.items), name='deptitems'),
    path('deleteitem/<int:id>/', views.deleteitem, name="deleteitem"),
    path('edititem/<int:id>/', views.edititem, name="edititem"),

    path('category/add/<int:id>/', views.addcategory, name="addcategory"),
    path('category/add/', views.addcategory, name="addnewcategory"),

    path('category/edit/<int:id>/', views.editcategory, name="editcategory"), 


    path('departments/', login_required(views.departments), name='departments'),
    path('deletedepartment/<int:id>/', views.deletedepartment, name="deletedepartment"),
    path('editdepartment/<int:id>/', views.editdepartment, name="editdepartment"),

]

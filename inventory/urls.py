from django.urls import path
from django.contrib.auth.decorators import login_required
from inventory import views
urlpatterns = [
    
    
    path('items/<int:id>/export/pdf/', login_required(views.export_pdf), name='export_dpt_pdf'),
    path('items/export/pdf/', login_required(views.export_pdf), name='export_pdf'),

    
    path('', login_required(views.index), name='index'),
    path('items/', login_required(views.items), name='items'),
    path('items/<int:id>/', login_required(views.items), name='deptitems'),
    path('deleteitem/<int:id>/', views.deleteitem, name="deleteitem"),
    path('edititem/<int:id>/', views.edititem, name="edititem"),

    path('category/add/<int:id>/', views.addcategory, name="addcategory"),
    path('category/add/', views.addcategory, name="addnewcategory"),
    path('category/edit/<int:id>/', views.editcategory, name="editcategory"), 
    path('category/delete/<int:id>/', views.deletecategory, name="deletecategory"), 


    path('inventories/', login_required(views.inventories), name='inventories'),
    path('deleteinventory/<int:id>/', views.deleteinventory, name="deleteinventory"),
    path('editinventory/<int:id>/', views.editinventory, name="editinventory"),

]
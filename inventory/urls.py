from django.urls import path
from django.contrib.auth.decorators import login_required
from inventory import views
from django.contrib.auth.decorators import login_required, user_passes_test

def is_superuser(user):
    return user.is_superuser

urlpatterns = [
    
    
    path('items/<int:id>/export/pdf/', login_required(views.export_pdf), name='export_dpt_pdf'),
    path('items/export/pdf/', user_passes_test(is_superuser)(views.export_pdf), name='export_pdf'),
    
    path('', login_required(views.index), name='index'),
    
    path('items/', user_passes_test(is_superuser)(views.items), name='items'),
    path('items/<int:id>/', login_required(views.items), name='deptitems'),
    path('deleteitem/<int:id>/', user_passes_test(is_superuser)(views.deleteitem), name="deleteitem"),
    path('deleteitemsinventory/<int:id>/', login_required(views.deleteitemsinventory), name="deleteitemsinventory"),
    path('additem/', user_passes_test(is_superuser)(views.additem), name='additem'),
    path('edititem/<int:id>/', user_passes_test(is_superuser)(views.edititem), name="edititem"),
    path('edititeminventory/<int:id>/', login_required(views.edititeminventory), name="edititeminventory"),


    path('categories/', user_passes_test(is_superuser)(views.categories), name='categories'),
    path('category/add/<int:id>/', user_passes_test(is_superuser)(views.addcategory), name="addcategory"),
    path('category/add/', user_passes_test(is_superuser)(views.addcategory), name="addnewcategory"),
    path('category/edit/<int:id>/', user_passes_test(is_superuser)(views.editcategory), name="editcategory"), 
    path('category/delete/<int:id>/', user_passes_test(is_superuser)(views.deletecategory), name="deletecategory"), 

    path('inventories/', user_passes_test(is_superuser)(views.inventories), name='inventories'),
    path('deleteinventory/<int:id>/', user_passes_test(is_superuser)(views.deleteinventory), name="deleteinventory"),
    path('editinventory/<int:id>/', login_required(views.editinventory), name="editinventory"),

]
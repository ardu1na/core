from django.contrib import admin
from inventory.models import Department, Inventory, Category, Item

# define info show in admin panel
admin.site.site_header = 'College Inventory System'
admin.site.index_title = 'Home'
admin.site.site_title = 'College Inventory System'



admin.site.register(Department)
                   
admin.site.register(Category)
                     
admin.site.register(Item)
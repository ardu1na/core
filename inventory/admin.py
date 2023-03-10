from django.contrib import admin
from inventory.models import Department, Inventory, Category, Item

# define info show in admin panel
admin.site.site_header = 'College Inventory System'
admin.site.index_title = 'Home'
admin.site.site_title = 'College Inventory System'


# create inventory crud management to department
class InventoryInstanceInline(admin.StackedInline):
    model = Inventory
    extra = 0
    show_change_link = True
    

class DepartmentAdmin(admin.ModelAdmin):
    inlines= [InventoryInstanceInline,]     
admin.site.register(Department, DepartmentAdmin)



admin.site.register(Inventory)
                     
admin.site.register(Category)
                     
admin.site.register(Item)
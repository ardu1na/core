from django.contrib import admin
from inventory.models import Category, Item, Inventory, ItemInventory

# define info show in admin panel
admin.site.site_header = 'Inventory System'
admin.site.index_title = 'Home'
admin.site.site_title = 'Inventory System'

class ItemInventoryAdmin (admin.TabularInline):
    model = ItemInventory
    extra = 1  

class InventoryAdmin(admin.ModelAdmin):
    inlines = ItemInventoryAdmin,  
admin.site.register(Inventory, InventoryAdmin)


admin.site.register(Category)
admin.site.register(Item)

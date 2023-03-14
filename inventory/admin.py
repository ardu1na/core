from django.contrib import admin
from inventory.models import Item, Inventory, ItemInventory

# define info show in admin panel
admin.site.site_header = 'College Inventory System'
admin.site.index_title = 'Home'
admin.site.site_title = 'College Inventory System'

class ItemInventoryAdmin (admin.TabularInline):
    model = ItemInventory


class InventoryAdmin(admin.ModelAdmin):
    inlines = ItemInventoryAdmin,
    
admin.site.register(Inventory, InventoryAdmin)

admin.site.register(Item)

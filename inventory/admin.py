from django.contrib import admin
from inventory.models import Department, Category, Item, Inventory

# define info show in admin panel
admin.site.site_header = 'College Inventory System'
admin.site.index_title = 'Home'
admin.site.site_title = 'College Inventory System'


class ItemInline(admin.StackedInline):
    model = Item.inventory.through
    extra = 0
    




@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline]



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'category')
    search_fields = ('name', 'category__name', 'inventory__name')
    list_filter = ('inventory__department', 'category')
    filter_horizontal = ('inventory',)


admin.site.register(Department)

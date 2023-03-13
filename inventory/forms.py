
from django import forms

from inventory.models import Item, Category, Inventory, ItemInventory

class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields = ('name',)
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"name",
                    'placeholder':"Name",
                    }),
        }
        
class AddItemForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
                    queryset=Item.objects.all(),
                    widget=forms.SelectMultiple(
                        attrs={
                                'class':"form-control",
                                'id':"item",
                                'placeholder':"items",
                                }),
                    )
    class Meta:
        model = Inventory
        fields = ('items',)
        

class ItemForm(forms.ModelForm):    
    category = forms.ModelChoiceField(
                    queryset=Category.objects.all(),
                    widget=forms.Select(
                        attrs={
                                'class':"form-control",
                                'id':"category",
                                'placeholder':"category",
                                }),
                    empty_label = 'None',
                    required=False)
    class Meta:
        model = Item
        fields = ('name', 'category', 'total')
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"name",
                    'placeholder':"Name",
                    }),
            'total' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"total",
                    'placeholder':"Quantity",
                    }),
        }




class InventoryForm(forms.ModelForm):
    
    class Meta:
        model = Inventory
        fields = ('department',)
        widgets = {
            'department' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"department",
                    'placeholder':"Department",
                    }),
        }
        
        
        
class ItemInventoryForm(forms.ModelForm):
    item = forms.ModelChoiceField(
                    queryset=Item.objects.all(),
                    widget=forms.Select(
                        attrs={
                                'class':"form-control",
                                'id':"item",
                                'placeholder':"item",
                                }),
        
                    )
    
    class Meta:
        model = ItemInventory
        fields = ('item', 'amount', 'inventory')
        widgets = {
            'amount' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"amount",
                    'placeholder':"Quantity",
                    }),
            'inventory': forms.HiddenInput(),  

        }
        
        
    
        
class EditItemInventoryForm(forms.ModelForm):
    
    class Meta:
        model = ItemInventory
        fields = ('amount', 'inventory', 'item')
        widgets = {
            'amount' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"amount",
                    'placeholder':"Quantity",
                    }),
            'inventory': forms.HiddenInput(),  
            'item': forms.HiddenInput(),  

        }
        


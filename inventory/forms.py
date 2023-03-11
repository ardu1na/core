
from django import forms

from inventory.models import Item, Category, Department, Inventory

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
        fields = ('name', 'category',)
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"name",
                    'placeholder':"Name",
                    }),
        }




class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)
        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'id':"name",
                    'placeholder':"Name",
                    }),
        }
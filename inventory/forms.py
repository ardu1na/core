
from django import forms

from inventory.models import Item, Category, Department


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

from django import forms

from inventory.models import Item, Category


class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
                                    'class':"form-control",
                                    'id':"category",
                                    'placeholder':"category",}),
                                empty_label = 'Assign a category',
                                required=False)
    
    class Meta:
        model = Item

        fields = ('name', 'category',)
        
        widgets = {

            'name' : forms.TextInput(attrs={'class':"form-control",
            'id':"name",
            'placeholder':"Name",}),
        }

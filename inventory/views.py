from django.shortcuts import render, redirect
from  django.urls import reverse
from django.http import HttpResponseBadRequest


from inventory.models import Item, Department
from inventory.forms import ItemForm


def index(request):    
    return render (request, 'index.html', {})





def items(request):
    items = Item.objects.all()
    addform=ItemForm()

    if request.method == 'GET':
        addform = ItemForm()
        
    if request.method == 'POST':
        if "additem" in request.POST:
            addform = ItemForm(request.POST)
            if addform.is_valid():
                addform.save()
                print(addform)
                return redirect(reverse('items')+ "?added")
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")
            
    data = {
        'items' : items,
        'addform' : addform,
    }
    return render (request, 'items.html', data)




def deleteitem(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect(reverse('items')+ "?deleted")







def departments(request):
    departments = Department.objects.all()
    data = {
        'departments' : departments,
    }
    return render (request, 'departments.html', data)
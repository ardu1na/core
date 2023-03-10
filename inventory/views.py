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
    search_query = request.GET.get('q')

    if search_query:
        items = items.filter(name__icontains=search_query)

    if request.method == 'GET':
        addform = ItemForm()
        
    if request.method == 'POST':
        if "additem" in request.POST:
            addform = ItemForm(request.POST)
            if addform.is_valid():
                addform.save()
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



def edititem(request, id):
    edititem = Item.objects.get(id=id)

    if request.method == "GET":
        editform = ItemForm(instance=edititem)
        data = {
            'editform': editform,
            'edititem': edititem,
            'id': id,
            }
        return render (request, 'edititem.html', data)

    if request.method == 'POST':
        editform = ItemForm(request.POST, instance=edititem)
        if editform.is_valid():
            editform.save()
            return redirect(reverse('items')+ "?changed")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")






def departments(request):
    departments = Department.objects.all()
    data = {
        'departments' : departments,
    }
    return render (request, 'departments.html', data)
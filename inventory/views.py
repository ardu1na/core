from django.shortcuts import render

from inventory.models import Item






def index(request):
    items = Item.objects.all()
    data = {
        'items' : items,
    }
    return render (request, 'index.html', data)
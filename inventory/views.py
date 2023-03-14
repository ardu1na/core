from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models import Q
from django.db import IntegrityError
from django.core.paginator import Paginator

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from inventory.models import Item, Inventory, Category, ItemInventory
from inventory.forms import ItemForm, InventoryForm, CategoryForm,  ItemInventoryForm, EditItemInventoryForm



def index(request):    
    return render (request, 'index.html', {})




def export_pdf(request, id=None):
    
    search_query = request.GET.get('q')
    
    if id:
        inventory = get_object_or_404(Inventory, id=id)
        if search_query:
            items = Item.objects.filter(iteminventory__inventory__id=inventory.id).filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
            filename = f'{inventory.department.lower().replace(" ", "")}_inventory_search_{search_query.lower().replace(" ", "")}_report.pdf'
        else:
            items = Item.objects.filter(iteminventory__inventory__id=inventory.id)
            filename = f'{inventory.department.lower().replace(" ", "_")}_inventory_report.pdf'               
    else:
        if search_query:
            items = Item.objects.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
            filename = f'all_items_search_{search_query.lower().replace(" ", "_")}_report.pdf'
        else:
            items = Item.objects.all()
            filename = 'all_items_report.pdf'
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    table_data = [['ID', 'Name', 'Category', 'Created At', 'Last Updated']]
    for item in items:
        created_at = item.created_at.strftime("%d %b %Y %H:%M")
        updated_at = item.updated_at.strftime("%d %b %Y %H:%M")
        category_name = item.category.name if item.category else 'None'
        table_data.append([str(item.id), item.name, category_name, created_at, updated_at])
        table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('LEFTPADDING', (0, 1), (-1, -1), 5),
        ('RIGHTPADDING', (0, 1),(-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('ROWBACKGROUNDS', (0, 1), (-1, 1), [colors.grey, colors.grey]),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(pdf)
    return response



def items(request, id=None):
    if id:
        inventory = Inventory.objects.get(id=id)
        items = ItemInventory.objects.filter(inventory__id=inventory.id)
        if request.method == 'GET':
            addform = ItemInventoryForm(initial={'inventory': inventory})

        error_message = None
        if "additems" in request.POST:
            error_message = "ATENTION: There are not enough quantity of this item available!! Try to add less."
            addform = ItemInventoryForm(request.POST, initial={'inventory': editinventory})
            try:
                if addform.is_valid():
                    addform.save()
                    data = {
                        'addform': addform,
                        'id':id,
                    }
                    return redirect('deptitems', id=id)
                else:
                    raise IntegrityError("Invalid form")
            except IntegrityError:
                error_message = "ATENTION: There are not enough quantity of this item available!! Try to add less."
                addform = ItemInventoryForm(initial={'inventory': inventory})
                data = {
                    'items' : items,
                    'inventory' : inventory,
                    'addform': addform,
                    'total_items_count': items.count(),
                    'id': id,
                    'error_message': error_message,
                }
                return render(request, 'items.html', data)
        data = {
            'items' : items,
            'inventory' : inventory,
            'addform': addform,
            'total_items_count': items.count(),
            'id': id,
            'error_message': error_message,
        }        
            
        search_query = request.GET.get('q')

        if search_query:
            items = items.filter(Q(item__name__icontains=search_query) | Q(item__category__name__icontains=search_query))
            
        data = {
        'items' : items,
        'inventory' : inventory,
        'addform': addform,
        'total_items_count': items.count(),
        'id': id,    }

    else:
        items = Item.objects.all()               
        search_query = request.GET.get('q')
        if search_query:
            items = items.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
            
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
            'total_items_count': items.count(),
        }
    return render  (request, 'items.html', data)


def additem(request):
    addform = ItemForm()

    if request.method == 'GET':
            addform = ItemForm()
            
    if request.method == 'POST':
        if "additem" in request.POST:
            addform = ItemForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect('items')
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.") 
    data = {
        'addform' : addform,
    }
    return render  (request, 'additem.html', data)



def deleteitem(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect(reverse('items')+ "?deleted")


def deleteitemsinventory(request, id):
    item_inventory = ItemInventory.objects.get(id=id)
    item = item_inventory.item
    item.available += item_inventory.amount
    item.save()
    item_inventory.delete()
    id = item_inventory.inventory.id
    return redirect('deptitems', id=id) 


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
        
        
def edititeminventory(request, id):
    edititem = ItemInventory.objects.get(id=id)
    if request.method == "GET":
        editform = EditItemInventoryForm(instance=edititem)
        data = {
            'editform': editform,
            'edititem': edititem,
            'id': id,
            }
        return render (request, 'edititeminventory.html', data)

    if request.method == 'POST':
        editform = EditItemInventoryForm(request.POST, instance=edititem)
        id_inv = edititem.inventory.id
        try:
            if editform.is_valid():
                editform.save()
                return redirect('deptitems', id=id_inv)
            else:
                raise IntegrityError("Invalid form")
        except IntegrityError:
            error_message = "ATENTION: There are not enough quantity of this item available!! Try to add less."
            data = {
                'error_message' : error_message,
                'edititem' : edititem,
                'editform' : editform,
                'id' : id_inv
            }
            return render (request, 'edititeminventory.html', data)



def categories(request):
    category_list = Category.objects.all()
    paginator = Paginator(category_list, 10) 
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    if request.method == 'GET':
        form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('categories')+ "?added")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.") 
    data = {
        'categories' : categories,
        'form' : form,
    }    
    return render (request, 'categories.html', data)


def addcategory(request, id=None):
    if id:
        item = Item.objects.get(id=id)
        if request.method == "GET":
            addform = CategoryForm()
        if request.method == 'POST':
            addform = CategoryForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('edititem', args=[id]) + "?newcategory")
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")
    else:
        if request.method == "GET":
            addform = CategoryForm()
        if request.method == 'POST':
            addform = CategoryForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('categories') + "?newcategory")
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")       
    data = {
            'addform': addform,
            }
    return render (request, 'addcategory.html', data)


def editcategory(request, id):
    category = Category.objects.get(id=id)
    if request.method == "GET":
        editform = CategoryForm(instance=category)
        data = {
            'editform': editform,
            'category': category,
            'id': id,
            }
        return render (request, 'editcategory.html', data)

    if request.method == 'POST':
        editform = CategoryForm(request.POST, instance=category)
        if editform.is_valid():
            editform.save()
            return redirect(reverse('categories')+ "?changed")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")


def deletecategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(reverse('categories')+ "?categorydeleted")






def inventories(request):
    inventories = Inventory.objects.all()
    addform=InventoryForm()
    search_query = request.GET.get('q')

    if search_query:
        inventories = inventories.filter(department__icontains=search_query)

    if request.method == 'GET':
        addform = InventoryForm()
        
    if request.method == 'POST':
        if "addinventory" in request.POST:
            addform = InventoryForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('inventories')+ "?added")
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.") 
    data = {
        'inventories' : inventories,
        'addform' : addform,
    }
    return render (request, 'inventories.html', data)


def deleteinventory(request, id):
    inventory = Inventory.objects.get(id=id)
    inventory.delete()
    return redirect(reverse('inventories')+ "?deleted")


def editinventory(request, id):
    editinventory = Inventory.objects.get(id=id)
    itemsinventory = ItemInventory.objects.filter(inventory=editinventory)
    
    if request.method == "GET":
        editform = InventoryForm(instance=editinventory)
        addform = ItemInventoryForm(initial={'inventory': editinventory})
        data = {
            'itemsinventory':itemsinventory,
            'addform' : addform,
            'editform': editform,
            'editinventory': editinventory,
            'id': id,
        }
        return render (request, 'editinventory.html', data)

    if request.method == 'POST':
        addform = ItemInventoryForm(initial={'inventory': editinventory})
        editform = InventoryForm(instance=editinventory)
        editinventory = Inventory.objects.get(id=id)

        if "additems" in request.POST:
            addform = ItemInventoryForm(request.POST, initial={'inventory': editinventory})
            try:
                if addform.is_valid():
                    addform.save()
                else:
                    raise IntegrityError("Invalid form")
            except IntegrityError:
                error_message = "ATENTION: There are not enough quantity of this item available!! Try to add less."
                data = {
                    'addform': addform,
                    'editform': editform,
                    'editinventory': editinventory,
                    'id': id,
                    'error_message': error_message,
                    'itemsinventory':itemsinventory,

                }
                return render(request, 'editinventory.html', data)

            data = {
                'addform': ItemInventoryForm(initial={'inventory': editinventory}),
                'editform': InventoryForm(instance=editinventory),
                'editinventory': editinventory,
                'id': id,
                'itemsinventory':itemsinventory,

            }
            return render(request, 'editinventory.html', data)

        editform = InventoryForm(request.POST, instance=editinventory)
        if editform.is_valid():
            editform.save()
            return redirect(reverse('inventories')+ "?changed")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")

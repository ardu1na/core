from io import BytesIO

from django.shortcuts import render, redirect
from  django.urls import reverse
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.http import HttpResponse
from django.db import IntegrityError

from reportlab.pdfgen import canvas

from inventory.models import Item, Inventory, Category, ItemInventory
from inventory.forms import ItemForm, InventoryForm, CategoryForm, AddItemForm, ItemInventoryForm

def index(request):    
    return render (request, 'index.html', {})

def export_pdf(request, id=None):
    # Get the data to include in the PDF document
    search_query = request.GET.get('q')

    if id:
        inventory = Inventory.objects.get(id=id)

        if search_query:
            items = Item.objects.filter(iteminventory__inventory__id=inventory.id).filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
            filename = f'{inventory.department.lower().replace(" ", "_")}_inventory_search_{search_query.lower().replace(" ", "_")}_report.pdf'
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

    # Create a BytesIO object to write the PDF document to
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = canvas.Canvas(buffer)

    # Draw the content onto the PDF
    if id:
        pdf.drawString(100, 750, f"{inventory.department} Inventory Report")
    else:
        pdf.drawString(100, 750, "All Items Report")

    pdf.drawString(100, 700, "Items:")
    max_width = 400

    y = 650
    for item in items:
        a = item.created_at
        created_at = a.strftime("%d %b %Y %H:%M")
        b = item.updated_at
        updated_at = b.strftime("%d %b %Y %H:%M")

       
        if item.category:
            text = f"## id: {item.id} - {item.name} - {item.category.name} - Created at: {created_at} - Last Updated: {updated_at}"
        else:
            text = f"## id: {item.id} -  {item.name} - None Category  - Created at: {created_at} - Last Updated: {updated_at}"

        # Split the text into lines that fit within the maximum width
        lines = []
        line = ''
        for word in text.split():
            if pdf.stringWidth(line + ' ' + word) <= max_width:
                line += ' ' + word if line else word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

        # Draw each line of the text block on the PDF
        for line in lines:
            pdf.drawString(20, y, line)
            y -= 20
        
    # Close the PDF object cleanly, and we're done.
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
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
                    print(addform.errors)

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
                print(addform.errors)
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
        'id': id,

    }

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
                return redirect(reverse('items') + "?newcategory")
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
            return redirect(reverse('items')+ "?changed")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")


def deletecategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(reverse('items')+ "?categorydeleted")


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

from io import BytesIO

from django.shortcuts import render, redirect
from  django.urls import reverse
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from inventory.models import Item, Department, Inventory, Category
from inventory.forms import ItemForm, DepartmentForm, CategoryForm, AddItemForm

def export_pdf(request, id=None):
    # Get the data to include in the PDF document
    if id:
        inventory = Inventory.objects.get(id=id)
        items = Item.objects.filter(inventory__id=inventory.id)
        # ...
    else:
        items = Item.objects.all()
        # ...

    # Create a BytesIO object to write the PDF document to
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = canvas.Canvas(buffer)

    # Draw the content onto the PDF
    if id:

        pdf.drawString(100, 750, f"{inventory} Inventory Report")
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

        """ if item.category:
            pdf.drawString(20, y, f"id: {item.id} - {item.name} - {item.category.name} - Created at: {created_at} - Last Updated: {updated_at}")
        else:
            pdf.drawString(120, y, f"id: {item.id} -  {item.name} - None Category  - Created at: {created_at} - Last Updated: {updated_at}")
        y -= 20"""
        
        if item.category:
            text = f"id: {item.id} - {item.name} - {item.category.name} - Created at: {created_at} - Last Updated: {updated_at}"
        else:
            text = f"id: {item.id} -  {item.name} - None Category  - Created at: {created_at} - Last Updated: {updated_at}"

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
    response['Content-Disposition'] = f'attachment; filename=inventory_report.pdf'
    return response


def index(request):    
    return render (request, 'index.html', {})



def items(request, id=None):
    if id:
        inventory = Inventory.objects.get(id=id)
        items = Item.objects.filter(inventory__id=inventory.id)
        if request.method == 'GET':
            addform = AddItemForm()

        if request.method == 'POST':
            if "additems" in request.POST:
                addform = AddItemForm(request.POST)
                if addform.is_valid():
                    add_items = addform.cleaned_data['items']
                    inventory.items.add(*add_items) # add new items to existing related objects
                    return redirect('deptitems', id=id)  

                else:
                    return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")

        search_query = request.GET.get('q')

        if search_query:
            items = items.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
            
        data = {
        'items' : items,
        'inventory' : inventory,
        'addform': addform
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
        }
    return render  (request, 'items.html', data)



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



def departments(request):
    departments = Department.objects.all()
    addform=DepartmentForm()
    search_query = request.GET.get('q')

    if search_query:
        departments = departments.filter(name__icontains=search_query)

    if request.method == 'GET':
        addform = DepartmentForm()
        
    if request.method == 'POST':
        if "adddepartment" in request.POST:
            addform = DepartmentForm(request.POST)
            if addform.is_valid():
                addform.save()
                return redirect(reverse('departments')+ "?added")
            else:
                return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.") 
    data = {
        'departments' : departments,
        'addform' : addform,
    }
    return render (request, 'departments.html', data)



def deletedepartment(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return redirect(reverse('departments')+ "?deleted")



def editdepartment(request, id):
    editdepartment = Department.objects.get(id=id)

    if request.method == "GET":
        editform = DepartmentForm(instance=editdepartment)
        data = {
            'editform': editform,
            'editdepartment': editdepartment,
            'id': id,
            }
        return render (request, 'editdepartment.html', data)

    if request.method == 'POST':
        editform = DepartmentForm(request.POST, instance=editdepartment)
        if editform.is_valid():
            editform.save()
            return redirect(reverse('departments')+ "?changed")
        else:
            return HttpResponseBadRequest("Ups! something gets wrong, go back and try again please.")
from django.db import models


class Department (models.Model):
    name = models.CharField(max_length=100, unique=True) # can't name a departament as any other departament
    
    def __str__ (self): # Define what to show when the department is called in a template without fields 
        return self.name




class Inventory (models.Model):
    name = models.CharField(
                            max_length=100,
                            unique=True                 # can't name a new list as any of other list
                            )
    department = models.OneToOneField(
                            Department,                 # one department has one list, in the first message say it has to be
                                                        # fk but if each department has just one inventorylist, this is better
                            
                            on_delete=models.CASCADE,   # if department is deleted, delete the list
                            null= True, blank= True)
    
    def __str__ (self): # Define what to show when the inventory is called in a template without fields
        return self.name





class Category (models.Model):
    name = models.CharField(max_length=100,
                            unique=True)    # can't name a new category as previous categories
    
    def __str__ (self):                     # Define what to show when the category is called in a template without fields
        return self.name





class Item (models.Model):
    name = models.CharField(max_length=100,
                            unique=True)                # can't name a new item as any of previous items
    
    created_at = models.DateTimeField(
                            auto_now_add=True)          # Automatically set the field to now when the item is first created.
    updated_at = models.DateTimeField(
                            auto_now=True)              # Automatically set the field to now every time the item is saved.
    
    inventory = models.ManyToManyField(
                                Inventory,             # one inventory has many items and one item could be in many inventories
                                null= True, blank= True,
                                related_name="items")       # how to call all items from Inventory
                                                            # ex: inventory.items return all items of a desired Inventory 
    
    category = models.ForeignKey(
                                Category,                   # one category has many items
                                on_delete=models.SET_NULL,  # if category is deleted, set category null
                                null= True, blank= True,
                                related_name="items")       # how to call all items from category
                                                            # ex: category.items return all items of a desired category 
     
     
    def __str__ (self): # Define what to show when the item is called in a template without fields 
        return self.name
    
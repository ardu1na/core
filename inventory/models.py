from django.db import models


class Department (models.Model):
    name = models.CharField(max_length=100, unique=True) # can't name a departament as any other departament
    
    def __str__ (self): # Define what to show when the department is called in a template without fields 
        return self.name       
    
    def save(self, *args, **kwargs):
        creating = self.pk is None          # check if the department is being created or updated                                            
        super().save(*args, **kwargs)       # each time we save the instance
        
        if creating:                        # when a new department is created
            Inventory.objects.create(name=self.name, department=self) 
                                            # a new Inventory will be auto created with the same name
                                            # and auto associated with its department.



class Inventory (models.Model):
    name = models.CharField(
                            max_length=100,
                            editable=False              # we auto create each department inventory 
                            )
    department = models.OneToOneField(
                            Department,                 # one department could have one inventory
                            
                            on_delete=models.CASCADE,   # if department is deleted, delete its inventory
                            null= True, blank= True) 
        
    def __str__ (self): # Define what to show when the inventory is called in a template without fields
         return f"{self.name} department inventory" # ex: if name is "science" it'll return "Science department inventory"

    class Meta:
        verbose_name_plural = "inventory lists" # Define the plural name show in admin panel
        
    




class Category (models.Model):
    name = models.CharField(max_length=100,
                            unique=True)    # can't name a new category as previous categories 
    def __str__ (self):                    
        return self.name  # Define what to show when the category is called in a template without fields
    class Meta:
        verbose_name_plural = "categories" # Define the plural name show in admin panel



class Item (models.Model):
    name = models.CharField(max_length=100,
                            unique=True)                # can't name a new item as any of previous items
    
    created_at = models.DateTimeField(auto_now_add=True)          # Automatically set the field to now when the item is first created.
    updated_at = models.DateTimeField(auto_now=True)              # Automatically set the field to now every time the item is saved.
       
       
    inventory = models.ManyToManyField(                     # one inventory has many items and one item could be in many inventories
                                Inventory,                  
                                related_name="items")       # how to call all items from a Inventory
                                                            # ex: inventory.items return all items of a desired Inventory 
    
       
    category = models.ForeignKey(                           # one category has many items but one item just has one category
                                Category,                   
                                on_delete=models.SET_NULL,  # if category is deleted, set category null
                                null= True, blank= True,
                                related_name="items")       # how to call all items from a category
                                                            # ex: category.items return all items of a desired category 
     
     
    def __str__ (self): # Define what to show when the item is called in a template without fields 
        return self.name
    
    
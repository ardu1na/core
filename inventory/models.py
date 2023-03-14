from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    
    
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    total = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)          # Automatically set the field to now when the item is first created.
    updated_at = models.DateTimeField(auto_now=True)              # Automatically set the field to now every time the item is saved.

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # if creating a new instance
            self.available = self.total
        elif self.total != self._original_total:  # if total is modified
            self.available += self.total - self._original_total
        super(Item, self).save(*args, **kwargs)
        self._original_total = self.total  # save the original value of total

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self._original_total = self.total  # save the original value of total



class Inventory(models.Model):
    department = models.CharField(max_length=150, unique=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="inventory")

    items = models.ManyToManyField(Item, through='ItemInventory', related_name="inventories")

    def __str__(self):
        return f"{self.department} Inventory"
    
    
        
    def save(self, *args, **kwargs):
        if not self.user:
            self.user = User.objects.create_user(
                username=self.department.lower().replace(' ', '_'),
                email="",
                password=f"{self.department.lower().replace(' ', '_')}_pass",
                first_name='',
                last_name='',
                is_active = True,
                is_staff = True,
            )
            self.id = self.user.id
            self.user.save()
        super().save(*args, **kwargs)





class ItemInventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} on {self.inventory.department} inventory"

    def clean(self):
        super().clean()
        if not self.pk:  # if creating a new instance
            self.item.available -= self.amount
        else:
            original_instance = ItemInventory.objects.get(pk=self.pk)
            self.item.available += original_instance.amount - self.amount

        if self.item.available < 0:
            raise ValidationError("Amount exceeds available quantity of the item.")

    def save(self, *args, **kwargs):
        super(ItemInventory, self).save(*args, **kwargs)
        self.item.save()  # save the updated available field in Item model

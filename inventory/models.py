from django.db import models
from django.core.exceptions import ValidationError

# This represents the item itself.
class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=40, unique=True) # SKU = Stock Keeping Unit
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
# This records history.
class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.PositiveIntegerField()
    movement_choices = [
        ("In","In"),
        ("Out","Out"),
    ]
    movement_type = models.CharField(max_length=3, choices=movement_choices, default=None)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def clean(self):
        if self.movement_type == "Out":
            if hasattr(self, 'product') and self.product:
                if self.quantity > self.product.quantity:
                    raise ValidationError(f"Not Enough Stock. Current: {self.product.quantity}")
                
    def save(self, *args, **kwargs):
        self.full_clean()   # Forces the clean method to run even if not using a Form
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movement_type} - {self.quantity} - {self.product.name}"
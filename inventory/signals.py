from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import StockMovement

@receiver(post_save, sender=StockMovement)
def update_stock(sender, instance, created, **kwargs):
    """
    sender: The model class (StockMovement)
    instance: The actual record being saved(the specific "In - 10" movement)
    created: Boolean. True if this is a new record. False if it's an update
    """

    # We only want to adjust stock if a new movement is created
    # If we are just editing a note on an old movement, we shouldn't add stock again
    if created:
        product = instance.product

        # Check if instance.movement_type is "In" or "Out"
        if instance.movement_type == "In":
            product.quantity += instance.quantity

        elif instance.movement_type == "Out":
            product.quantity -= instance.quantity

            if product.quantity <= product.low_stock_threshold:
                print(f"ALERT: Low stock for {product.name}! ({product.quantity} left)")

        
        product.save()
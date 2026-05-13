from django.db import models

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('UPI / QR Code', 'UPI / QR Code'),
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Card Payment', 'Card Payment'),
    ]

    order_id       = models.AutoField(primary_key=True)
    customer_name  = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=15)
    table_number   = models.CharField(max_length=20)
    payment_type   = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    items_ordered  = models.TextField()        # stored as JSON string
    total_amount   = models.IntegerField()
    ordered_at     = models.DateTimeField(auto_now_add=True)
    is_paid        = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order_id} | {self.customer_name} | {self.table_number}"

    class Meta:
        ordering = ['-ordered_at']
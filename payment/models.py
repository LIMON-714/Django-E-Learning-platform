from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = [
        ("Card", "Card"),
        ("Bkash", "Bkash"),
        ("Nagad", "Nagad"),
        ("Rocket", "Rocket"),
        ("Paypal", "Paypal"),
    ]

    # User Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Payment Details
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    card_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    paypal_email = models.EmailField(blank=True, null=True)

    # Course and amount
    course_name = models.CharField(max_length=250, blank=True, null=True)
    course_slug = models.SlugField(blank=True, null=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course_name}"

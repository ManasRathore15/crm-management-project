from django.db import models

# Create your models here.

class Lead(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]

    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    service = models.CharField(max_length=20)
    message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
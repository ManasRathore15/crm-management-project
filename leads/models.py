from django.db import models

# Create your models here.

class Lead(models.Model):

    STATUS_CHOICES = [
    ('NEW', 'New'),
    ('CONTACTED', 'Contacted'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
    ('REJECTED', 'Rejected'),
]

    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    service = models.CharField(max_length=50)
    message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
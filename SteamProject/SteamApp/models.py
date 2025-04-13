from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('RPG', 'Role Playing Game'),
        ('Strategy', 'Strategy'),
        ('Sports', 'Sports'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=255, unique=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length= 255, default= "")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)  # Added for tracking
    visited= models.IntegerField(default= 0)
    revenue= models.DecimalField(max_digits= 10, decimal_places= 4, default= 0)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-visited']),
        ]

    def __str__(self):
        return f'{self.name} by {self.publisher.username} - {self.price}$'
    
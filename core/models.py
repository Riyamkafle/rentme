from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Property(models.Model):
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    image = models.ImageField(upload_to='img')
    available_for_rent = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
    


class BookProperty(models.Model): 
    owner = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "owner")
    renter = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "renter")
    property = models.ForeignKey(Property,on_delete = models.CASCADE)

    # def __str__(self): 
    #     return f"{self.owner.username}-{self.renter.username}-{self.property.title}"
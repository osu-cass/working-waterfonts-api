from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PointOfInterest(models.Model):

    def __unicode__(self):
        return self.name

    name = models.TextField()
    alt_name = models.TextField(blank=True)
    description = models.TextField()
    history = models.TextField()
    facts = models.TextField()

    # Geo Django field to store a point
    location = models.PointField()
    objects = models.GeoManager()

    street = models.TextField()
    city = models.TextField()
    state = models.TextField()
    location_description = models.TextField(blank=True)
    zip = models.TextField()

    contact_name = models.TextField()
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True, null=True)

    products_preparations = models.ManyToManyField(
        'Hazard', blank=True)
    products_preparations = models.ForeignKey("Category")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
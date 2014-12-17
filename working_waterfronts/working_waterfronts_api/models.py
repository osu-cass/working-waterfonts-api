from django.contrib.gis.db import models
from phonenumber_field.modelfields import PhoneNumberField


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

    hazards = models.ManyToManyField(
        'Hazard', blank=True)
    categories = models.ManyToManyField(
        'Category', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Video(models.Model):
    """
    The video model holds a video URL and related data.

    The Created and Modified time fields are created automatically by
    Django when the object is created or modified, and can not be altered.

    This model uses Django's built-ins for holding the video URL and
    data in the database, as well as for keeping created and modified
    timestamps.
    """

    def __unicode__(self):
        return self.caption

    video = models.URLField()
    caption = models.TextField(blank=True)
    name = models.TextField(default='')
    pointofinterest = models.ForeignKey('PointOfInterest')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return {
            'caption': self.caption,
            'name': self.name,
            'link': self.video
        }
<<<<<<< HEAD


class Image(models.Model):

    """
    The Image model holds an image and related data.

    The Created and Modified time fields are created automatically by
    Django when the object is created or modified, and can not be altered.

    This model uses Django's built-ins for holding the image location and
    data in the database, as well as for keeping created and modified
    timestamps.
    """

    def filename(self):
        return os.path.basename(self.image.name)

    def __unicode__(self):
        return self.name

    image = models.ImageField(upload_to='images')
    name = models.TextField(default='')
    caption = models.TextField(blank=True)
    pointofinterest = models.ForeignKey('PointOfInterest')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def natural_key(self):
        return {
            'name': self.name,
            'caption': self.caption,
            'link': self.image.url
        }


class Category(models.Model):
    """
    The category model is a name associated with many points of interest.
    Its raison d'etre is to be a category for POIs -- it holds no other
    information itself.
    """

    def __unicode__(self):
        return self.category

    category = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Hazard(models.Model):
    """
    The Hazard model holds a hazard and its description.
    """
    name = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

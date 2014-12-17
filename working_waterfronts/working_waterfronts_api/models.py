from django.db import models


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
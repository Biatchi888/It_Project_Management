from django.db import models
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField
from django.conf import settings
import os
from django.utils.text import slugify
from cloudinary.models import CloudinaryField



# Choice Fields
MEAL_TYPES = (("breakfast", "Breakfast"), ("lunch", "Lunch"), ("dinner", "Dinner"))
RECIPE_DIFFICULTY = (
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("advanced", "Advanced"),
    ("expert", "Expert"),
)               
CUISINE_TYPES = (
    ('american', 'American'),
    ('caribbean', 'Caribbean'),
    ('chinese', 'Chinese'),
    ('european', 'European'),
    ('filipino', 'Filipino'),
    ('french', 'French'),
    ('german', 'German'),
    ('greek', 'Greek'),
    ('indonesian', 'Indonesian'),
    ('italian', 'Italian'),
    ('japanese', 'Japanese'),
    ('korean', 'Korean'),
    ('lebanese', 'Lebanese'),
    ('mexican', 'Mexican'),
    ('spanish', 'Spanish'),
    ('thai', 'Thai'),
    ('vietnamese', 'Vietnamese'),
)
class Recipe(models.Model):
    """
    A model to create and manage recipes
    """

    user = models.ForeignKey(User, related_name="recipe_owner", on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    title = models.CharField(max_length=300, null=False, blank=False)    
    description = models.CharField(max_length=500, null=False, blank=False)
    instructions = RichTextField(max_length=10000, null=False, blank=False)
    ingredients = RichTextField(max_length=10000, null=False, blank=False)
    preptime_hours = models.IntegerField(null=False, blank=False,default=0)
    preptime_minutes = models.IntegerField(null=False, blank=False,default=0)
    total_preptime = models.IntegerField(null=False, blank=False, editable=False)  # Make the field non-editable

    servings = models.IntegerField(null=False, blank=False)
    cooktime_hours = models.IntegerField(null=False, blank=False,default=0)
    cooktime_minutes = models.IntegerField(null=False, blank=False,default=0)
    total_cooktime = models.IntegerField(null=False, blank=False, default=0,editable=False)  # Make the field non-editable

    price = models.IntegerField(null=False, blank=False)
    image = CloudinaryField('image', 
            transformation=[
                {'width': 400, 'crop': 'limit', 'quality': 'auto'}
            ],
            null=False, 
            blank=False
        )
    image_url = models.URLField(max_length=500, blank=True, null=True)

    image_alt = models.CharField(max_length=100, null=False, blank=False)
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPES, default="breakfast")
    recipe_difficulty = models.CharField(max_length=50, choices=RECIPE_DIFFICULTY, default="beginner")
    cuisine_types = models.CharField( max_length=50, choices=CUISINE_TYPES, default="african")
    calories = models.IntegerField()
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_meal_type_counts(cls):
        return cls.objects.values("meal_type").annotate(count=models.Count("id"))
    def save(self, *args, **kwargs):
        if not self.preptime_hours and not self.preptime_minutes:
            self.total_preptime = 0
        elif not self.preptime_hours:
            self.total_preptime = self.preptime_minutes
        elif not self.preptime_minutes:
            self.total_preptime = self.preptime_hours * 60
        else:
            total_minutes = self.preptime_hours * 60 + self.preptime_minutes
            self.total_preptime = total_minutes

        if not self.cooktime_hours and not self.cooktime_minutes:
            self.total_cooktime = 0
        elif not self.cooktime_hours:
            self.total_cooktime = self.cooktime_minutes
        elif not self.cooktime_minutes:
            self.total_cooktime = self.cooktime_hours * 60
        else:
            total_cooktime = self.cooktime_hours * 60 + self.cooktime_minutes
            self.total_cooktime = total_cooktime

        super().save(*args, **kwargs)
        if self.image:
            self.image_url = self.image.url  # Get Cloudinary image URL
            super().save(update_fields=['image_url'])

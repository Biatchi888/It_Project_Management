from django.db import models
from djrichtextfield.models import RichTextField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    """Profile model"""
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )

    CIVIL_STATUS_CHOICES = (
        ("Single", "Single"),
        ("Married", "Married"),
        ("Widowed", "Widowed"),
        ("Divorced", "Divorced"),
    )

    CUISINE_CHOICES = (
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

    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    image = CloudinaryField('image', 
            transformation=[
                {'width': 400, 'crop': 'limit', 'quality': 'auto'}
            ],
            null=False, 
            blank=False
        )
    image_url = models.URLField(max_length=500, blank=True, null=True)
    bio = RichTextField(max_length=2500, null=True, blank=True)

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="Others")
    civil_status = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES, default="Single")
    preferred_cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES, default="None")
    country = CountryField(default="PH")

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    """Create or update the user profile"""
    if created:
        Profile.objects.create(user=instance)

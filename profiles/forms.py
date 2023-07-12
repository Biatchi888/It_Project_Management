from django import forms
from .models import Profile
from django_countries.widgets import CountrySelectWidget
from django.forms.widgets import DateInput

class ProfileForm(forms.ModelForm):
    """Form to create a profile"""

    class Meta:
        model = Profile
        fields = ["image", "bio", "first_name", "last_name", "birthday", "age", "gender", "civil_status", "preferred_cuisine", "country"]
        labels = {
            "image": "Avatar",
            "bio": "Bio",
            "first_name": "First Name",
            "last_name": "Last Name",
            "birthday": "Birthday",
            "age": "Age",
            "gender": "Gender",
            "civil_status": "Civil Status",
            "preferred_cuisine": "Preferred Cuisine",
            "country": "Country",
        }
        widgets = {
            "country": CountrySelectWidget(),
            "birthday": DateInput(attrs={"type": "date"}),
        }
        
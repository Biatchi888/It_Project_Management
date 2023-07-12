from django.contrib import admin
from .models import Profile
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.db.models import Count
from django.core.exceptions import FieldError

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "bio", "image")
    change_list_template = 'admin/profiles/change_list.html'  # Path to your custom change_list.html template

    def changelist_view(self, request, extra_context=None):
        # Retrieve the name of the administrator
        admin_name = User.objects.filter(username=request.user.username).first().get_full_name()
        
        # Retrieve the profile details
        profiles = Profile.objects.all()
        profile_details = []

        # Retrieve gender, cuisine, and age data
        gender_data = {
            'Male': 0,
            'Female': 0,
            'Other': 0
        }
        cuisine_data = {}
        age_data = []
        age_counts = {}  # Initialize the age_counts dictionary

        
        for profile in profiles:
            # Update gender count
            gender = profile.gender
            if gender in gender_data:
                gender_data[gender] += 1

            # Update cuisine count
            cuisine = profile.preferred_cuisine
            if cuisine:
                cuisine_data[cuisine] = cuisine_data.get(cuisine, 0) + 1

            # Count users per age
            age = profile.age
            age_counts[age] = age_counts.get(age, 0) + 1

            # Create a dictionary with profile details
            profile_dict = {
                'user': {
                    'date_joined': profile.user.date_joined.isoformat(),
                },
            }
            profile_details.append(profile_dict)

        # Convert age counts to scatter plot data format
        age_data = [
            { 'age': age, 'users': count } for age, count in age_counts.items()
        ]

        # Convert data to JSON format
        gender_data_json = json.dumps(gender_data)
        cuisine_data_json = json.dumps(cuisine_data)
        age_data_json = json.dumps(age_data)

        # Get the user with the highest number of created recipes
        try:
            user_with_most_recipes = User.objects.annotate(recipe_count=Count('recipe_owner')).order_by('-recipe_count').first()
            user_with_most_recipe_count = getattr(user_with_most_recipes, 'recipe_count', 0)
        except FieldError:
            user_with_most_recipes = None

        # Get the preferred cuisine with the most number of users
        try:
            cuisine_with_most_users = max(cuisine_data, key=cuisine_data.get)
            cuisine_with_most_user_count = cuisine_data[cuisine_with_most_users]
        except ValueError:
            cuisine_with_most_users = None
            cuisine_with_most_user_count = 0
        
        extra_context = extra_context or {}
        extra_context['admin_name'] = admin_name
        extra_context['profile_details_json'] = JsonResponse(profile_details, safe=False).content.decode()
        extra_context['gender_data_json'] = gender_data_json
        extra_context['cuisine_data_json'] = cuisine_data_json
        extra_context['age_data_json'] = age_data_json
        extra_context['user_with_most_recipes'] = user_with_most_recipes
        extra_context['user_with_most_recipe_count'] = user_with_most_recipe_count
        extra_context['cuisine_with_most_users'] = cuisine_with_most_users
        extra_context['cuisine_with_most_user_count'] = cuisine_with_most_user_count
        
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Profile, ProfileAdmin)
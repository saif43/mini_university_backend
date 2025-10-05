from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# The User model is already registered by default, so we don't need to register it again
# But we can customize it if needed

# Custom User admin if needed in the future
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

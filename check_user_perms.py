
import os
import django

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create a dummy user
username = 'test_security_user_v2'
if User.objects.filter(username=username).exists():
    User.objects.get(username=username).delete()

# Simulating a normal signup (create_user)
user = User.objects.create_user(username=username, password='password', email='test@example.com')
print(f"User created: {user.username}")
print(f"is_staff: {user.is_staff}")
print(f"is_superuser: {user.is_superuser}")

if user.is_staff:
    print("WARNING: New users are created with is_staff=True (Admin Access Possible)")
elif user.is_superuser:
    print("WARNING: New users are created with is_superuser=True (Admin Access and More)")
else:
    print("SAFE: New users are regular users (is_staff=False, is_superuser=False).")


import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_project.settings')
django.setup()

# Force ALLOWED_HOSTS
settings.ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

from django.test import Client
from django.contrib.auth.models import User

# Create a regular user
username = 'regular_user_test'
password = 'password123'
try:
    if User.objects.filter(username=username).exists():
        User.objects.get(username=username).delete()
    
    user = User.objects.create_user(username=username, password=password)
    print(f"Created regular user: {username} (is_staff={user.is_staff})")
    
    c = Client()
    # Login
    logged_in = c.login(username=username, password=password)
    print(f"Login successful: {logged_in}")
    
    # Try to access admin dashboard
    # Note: Client.login() saves the session.
    response = c.get('/admin/', follow=True)
    
    # Check where we ended up
    # If successful login to admin, we'd be at /admin/
    # If rejected, likely /admin/login/?next=/admin/ 
    # But since we are already logged in as a regular user, Django Admin usually shows the login page again 
    # with a "You are authenticated as ... but are not authorized to access this page" error.
    
    final_url = response.redirect_chain[-1][0] if response.redirect_chain else response.request.get('PATH_INFO', '')
    print(f"Final URL: {final_url}")
    print(f"Status Code: {response.status_code}")
    
    content = response.content.decode('utf-8')
    
    if "Site administration" in content and "Recent actions" in content:
        print("RESULT: FAILURE - Regular user accessed Admin Dashboard!")
    elif "Log in" in content:
        print("RESULT: SUCCESS - Admin login page shown (Access Denied for regular user)")
        if "authenticated as" in content:
            print("  (Confirmed: User is authenticated but unauthorized)")
    else:
        print("RESULT: UNKNOWN - Check output manually")

except Exception as e:
    print(f"Error: {e}")

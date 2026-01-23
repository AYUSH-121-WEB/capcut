
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_project.settings')
django.setup()

# Hack ALLOWED_HOSTS for this test
settings.ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

from django.test import Client

c = Client()
response = c.get('/admin/', follow=True) # Follow redirects

print(f"Final URL: {response.request['PATH_INFO'] if 'PATH_INFO' in response.request else 'unknown'}")
# Note: Client.get() response doesn't always have request dict easily accessible as a dict in printed form, 
# but redirect_chain is available if follow=True

if response.redirect_chain:
    print(f"Redirect chain: {response.redirect_chain}")
    print("Result: SECURE (Redirected)")
else:
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        # Check if we landed on a login page or the admin dashboard
        content = response.content.decode('utf-8')
        if "Log in" in content or "password" in content.lower():
             print("Result: SECURE (Login Page)")
        else:
             print("Result: INSECURE (Dashboard accessible?)")
    else:
        print(f"Result: OTHER ({response.status_code})")

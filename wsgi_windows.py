activate_this = 'C:/xampp/htdocs/django/Lotus/lotusCoorperators/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/godofwebapps/AppData/Local/Programs/Python/Python38-32/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/xampp/htdocs/django/Lotus/lotusCoorperators')
sys.path.append('C:/xampp/htdocs/django/Lotus/lotusCoorperators/lotusCoorperators')

os.environ['DJANGO_SETTINGS_MODULE'] = 'lotusCoorperators.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lotusCoorperators.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
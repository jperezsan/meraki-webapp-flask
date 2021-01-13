#flaskapp.wsgi
  
import os

# Import env variables
# .env file with environment variables must be created

activate_this = '/var/www/html/flaskapp/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


import sys
sys.path.insert(0, '/var/www/html/flaskapp')

from flaskapp import app as application

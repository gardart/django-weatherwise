# Installation
Start the new Django Weatherwane application with a fresh database  

python manage.py reset weatherwane 
python manage.py syncdb 
python manage.py schemamigration weatherwane --initial 
python manage.py migrate weatherwane 
python manage.py runserver

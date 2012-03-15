Keyra testvefinn i bakgrunni
	$ nohup python projects/django-weatherwise/weatherwise/manage.py runserver vedur.teigur.com:8080 > /dev/null 2>&1 &

Bua til requirements skra fyrir virtualenv
	$ pip freeze -E django-weatherwise > requirements.txt

Setja upp koda med pip fra git slod inn i virtual python library
Daemi, python-metar
	$ pip install -e git://github.com/tomp/python-metar.git#egg=python-metar

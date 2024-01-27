
migrate:
	python manage.py migrate --settings=settings.local

runserver: migrate
	python manage.py runserver --settings=settings.local

makemigrations:
	python manage.py makemigrations --settings=settings.local

createsuperuser:
	python manage.py createsuperuser --settings=settings.local

tests:
	python manage.py test --settings=settings.local

login-view-test:
	python manage.py test accounts --settings=settings.local --exclude-tag=login

test-one:
	python manage.py test $(test) --settings=settings.local

shellplus:
	python manage.py shell_plus --ipython --settings=settings.local

mig:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

super:
	python manage.py createsuperuser

# command: make push m="commit message"
push:
	git add -A
	git commit -m "$(m)"
	git push origin master
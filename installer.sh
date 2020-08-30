pip3 install virtualenv

virtualenv venv

source venv/bin/active

pip3 install -r requirements.txt

python3 manage.py collectstatic

python3 manage.py makemigrations concept

python3 manage.py migrate concept

python3 manage.py runserver
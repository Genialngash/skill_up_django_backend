# Veeta-Backend

Set an environment variable with the key of 'VEETA_ENV' and value of 'core.settings.dev'

### Create a virtual environment

`python3 -m venv venv`

### Switch to the virtual env

`source venv/bin/activate`

### Install the dependencies

`pip install -r requirements.txt`

### Make the necessary migrations

`python manage.py makemigrations && python manage.py migrate`

### Create a Super User

With the venv activated, enter the following commands in the terminal

1. python manage.py createsuperuser
2. follow the prompts and enter your email, first_name, last_name and passwords

### populate db with fake data for testing

`python manage.py populatedb`
NB: Users created with populatedb have a default password of 'testing321'

### Run the app

`python manage.py runserver`

### API Documentation

To view the schema and the endpoints available, go to http://localhost:8000/api/schema/swagger

### Access the admin panel

Go to http://localhost:8000/admin to sign in with the new super user account

### Create Temporary Stripe Webhook

`stripe listen --forward-to localhost:8000/payments/webhook/`

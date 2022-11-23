This project is designed to help people travel between Russian cities without service fees, paying only for the trip itself directly to the driver.


After cloning the repository and successfully running the project in Docker, write the following commands in the console to perform migrations and collect static files:

1) docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
2) docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear


The application will be available at: http://localhost:1337

# Django_Exercise_Recipe_App
CRUD API so you can remember your favourtie recipes and what goes in them. Because sometimes that is HARD. Ability to GET, POST, UPDATE and DELETE Recipes and Ingredients.

# Set up

- Clone Repo
- Move to Directory
- Environment Variables - you will need to create a .env file in the root directory and add the below:
```
PASSWORD=<set your password here>
```
- Build Docker Image:
```
docker-compose build
```
- Start Docker Image:
```
- docker-compose up
```

# Tests
To run tests and linting:
```
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

# Endpoints

### /recipe/admin/
*To access the admin account, you will have to create a superuser by running the following command:*
```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
### /recipe/recipes/
### /recipe/recipes/{recipe-id}/
### /recipe/ingredients/

# Intelregion Assessment


## Features

- **Advanced Security**: The application, yet sinple, but endowed with layers of security

- **User Registration**: User can register with email, username and their password

- **User Authentication**: User authentication is provided using JWT. The authorization (access) token has to attached to a bearer. i.e 
Bearer <token>

- **Blog Creation**: Authenticated user have the permission to create blog

- **Comment Creation**: Authenticated user have the permission to add comment to bogs

- **Content Manipulation**: Authenticated user and author of a particular blog/comment can edit or delete the blog/comment 

- **Content Pagination**: Blogs and Comments are well paginated to return 10 items per page


## Testing
To run the test in the application, use the command below in the root directory of the application
`pytest`
This will run all the test cases

## CI/CD 
A continous integration configuration has been applied on this project so that it automatically run the test cases when it changes are pushed to the github. But it is required to set the secrets (SECRET_KEY and X-API-KEY) in the github.

If you wish to deploy to an heroku dynos. You just need to modify the workflow yml fille and provide the heroku credentials


## Installation

You need to configure your environmental varables before running the application. An example of .env file has been provided (env.txt). You need to create a file named `.env` in the root directory of the application and configure it based on the example env file.

**Running with docker**
When running with docker, A postgres instance is created, so you need to tell your application you are running using docker. This is a simple proccess, all you need to do is change the ENVIRONMENT variable in the .env file to `docker` 
1. The software runs on docker, so you must docker installed to use all the features. You can get to https://www.docker.com/ to get docker for your os
2. On your terminal, run - `docker compose up --build`
3. open your browser and go to http://127.0.0.1:8000 or localhost:8000

**Running directly on terminal**
You must make sure your ENVIRONMNET variable is not set to `docker` when you are using this approach, unless you are running a postgres instance that is configured based on your env file

1. create a virtual environment
2. run `pip install -r requirements.txt`
3. runserver with `python manage.py runserver`


## API Documentation

API documentation has been generated using postman to make interaction and testing easy. The documentation can be accessed through the link below

https://documenter.getpostman.com/view/30266713/2sA3kYifag

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started
### Structure

### Prerequisites and Installation

To be able to work on this project you must have

- python3

``` bash
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get install python3.6
```

- pip3
``` bash
sudo apt install python3-pip
```

#### Backend dependencies:
once your environment is ready either you are using a virtual environment or developing on the local machine without a virtual environment, you have to install the backend dependencies, navigate to the downloaded application directory, open the terminal and run:

``` bash
pip3 install -r requirements.txt
```

#### Export the environment variables
`setup.sh` file contains 
- the environmental variables that need to be exported to facilitate the development and testing process including
    - FLask_app : Name of flask application.
    - APP_SETTINGS : Application mode which in our case is `development`.
    - DATABASE_PATH : The database path used during development.
    -  TESTDATABASE_PATH : The test database path used in testing the application.
    - AUTH0_URL : Authorization URL used in [auth0](https://auth0.com/)
    - AUTH0_AUDIENCE : API used in [auth0](https://auth0.com/)
    - AUTH0_CLIENT_ID : Client ID used in [auth0](https://auth0.com/)
    -  CASTING_PRODUCER_JWT : Producer JWT used in development and testing.
    - CASTING_DIRECTOR_JWT : Director JWT used in development and testing.
    - CASTING_ASSISTANT_JWT : Assistant JWT used in development and testing.

**you have to update this file or the environmental variable with your information** `example domain,JWT`
``` bash
source setup.sh
```

#### Running the backend in development mode

``` bash
export FLASK_APP=__init__.py
export FLASK_ENV=development
flask run
```


#### Create Database

- This application uses a database called `capstoneDB`. 
```
psql
postgres=# CREATE DATABASE capstoneDB;
postgres=# \q
```
- apply the migrations, navigate to `app` folder

```
flask db init
flask db upgrade
```

### Testing 
- the application in testing dependes on unittest which is framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages.

- To run the tests, navigate to root of the application folder

``` bash
dropdb capstoneDB_test
createdb capstoneDB_test
source setup.sh
python3 test_app.py 
```

## API Reference

### Getting started
- Base URL: 
    - **Development** : The backend app is hosted at the default, http://127.0.0.1:5000/
    - **Production** : The application has domain and hosted using [heroku](https://www.heroku.com/)
- Authentication: This version of application required authentication and authorization and this is done through [auth0](https://auth0.com/)
    - The roles:
        - Casting Assistant
            - Can view actors and movies
        - Casting Director
            - All permissions a Casting Assistant has and…
            - Add or delete an actor from the database
            - Modify actors or movies
        - Executive Producer
            - All permissions a Casting Director has and…
            - Add or delete a movie from the database

    - List of Permissions (Scopes) on [auth0](https://auth0.com/)
        - get:movies
        - get:single-movie	
        - delete:movies
        - patch:movies	
        - post:movies	
        - get:actors
        - get:single-actor	
        - delete:actors	
        - patch:actors	
        - post:actors


### Error Handling
Errors are returned as JSON objects in the following format:

``` json
{
    "success": False,
    "error": 400,
    "message":"bad request"
}
```
The api will return eight error types when requests fail:
- 422: Unprocessable
- 404: Not found
- 400: Bad request
- 405: Not allowed
- 409: Conflict
- 401: Unauthorized
- 403: Forbidden
- 500: Internal server error


### Endpoints


##### GET /movies

- General: It returns list of movies.

- Sample: `curl -H "Authorization: $CASTING_DIRECTOR_JWT" http://127.0.0.1:5000/movies`

```json
{
  "movies": [
    {
      "id": 1, 
      "release_date": "Tue, 01 Jan 2008 00:00:01 GMT", 
      "title": "star war"
    }, 
    {
      "id": 2, 
      "release_date": "Tue, 01 Jan 2008 00:00:01 GMT", 
      "title": "gone girl"
    }, 
    {
      "id": 3, 
      "release_date": "Tue, 01 Jan 2008 00:00:01 GMT", 
      "title": "home alone"
    }, 
    {
      "id": 4, 
      "release_date": "Tue, 26 Oct 1993 00:00:00 GMT", 
      "title": "the skack"
    }, 
    {
      "id": 6, 
      "release_date": "Fri, 26 Oct 2018 00:00:00 GMT", 
      "title": "Frozen"
    }
  ], 
  "success": true
}
```

##### GET /movies/\<int:movie_id>

- General: It returns a single movie. 

- Sample:`curl -H "Authorization: $CASTING_DIRECTOR_JWT" http://127.0.0.1:5000/movies/1`

```json
{
  "movie": {
    "id": 1, 
    "release_date": "Tue, 01 Jan 2008 00:00:01 GMT", 
    "title": "star war"
  }, 
  "success": true
}
```

##### DELETE /movies/\<int:movie_id>

- General: 
    - It deletes a movie of specific Id 
    - Return the deleted movie object

- Sample:`curl -H "Authorization: $CASTING_PRODUCER_JWT" http://127.0.0.1:5000/movies/6 -X DELETE`

```json
{
  "movie": {
    "id": 6, 
    "release_date": "Fri, 26 Oct 2018 00:00:00 GMT", 
    "title": "Frozen"
  }, 
  "success": true
}
```

##### PATCH /movies/\<int:movie_id>

- General:
    - Updates a movie data.
    - Returns the updated movie.

- Sample:`curl -H "Authorization: $CASTING_PRODUCER_JWT" -H "Content-Type: application/json" -d '{"title": "star wars","release_date":"2014-12-4"}'  http://127.0.0.1:5000/movies/1 -X PATCH`

```json
{
  "movie": {
    "id": 1, 
    "release_date": "Thu, 04 Dec 2014 00:00:00 GMT", 
    "title": "star wars"
  }, 
  "success": true
}
```

##### POST /movies

- General: 
    -  Adds a new movie.
    -  Returns the added movie

- Sample: ` curl -H "Authorization: $CASTING_PRODUCER_JWT" -H "Content-Type: application/json" -d '{"title": "gone with the wind","release_date":"2014-12-4"}'  http://127.0.0.1:5000/movies -X POST`

```json
{
  "movie": {
    "id": 8, 
    "release_date": "Thu, 04 Dec 2014 00:00:00 GMT", 
    "title": "Gone With The Wind"
  }, 
  "success": true
}
```

##### GET /actors

- General:  It returns a list of actors

- Sample:`curl -H "Authorization: $CASTING_DIRECTOR_JWT" http://127.0.0.1:5000/actors`

```json
{
  "actors": [
    {
      "age": 26, 
      "gender": "F", 
      "id": 1, 
      "name": "Mira Samuel"
    }, 
    {
      "age": 26, 
      "gender": "F", 
      "id": 2, 
      "name": "Meena Shalaby"
    }, 
    {
      "age": 26, 
      "gender": "F", 
      "id": 3, 
      "name": "Youssra"
    }, 
    {
      "age": 40, 
      "gender": "M", 
      "id": 4, 
      "name": "Ahmed el Saka"
    }, 
    {
      "age": 42, 
      "gender": "M", 
      "id": 5, 
      "name": "Ahmed Zaki"
    }, 
    {
      "age": 66, 
      "gender": "F", 
      "id": 9, 
      "name": "Soad Hosny"
    }
  ], 
  "success": true
}
```


##### GET /actors/\<int:actor_id>

- General: It returns a single actor.

- Sample:`curl -H "Authorization: $CASTING_DIRECTOR_JWT" http://127.0.0.1:5000/actors/1`

```json
{
  "actor": {
    "age": 26, 
    "gender": "F", 
    "id": 1, 
    "name": "Mira Samuel"
  }, 
  "success": true
}
```


##### DELETE /actors/\<int:actor_id>

- General: 
    - Deletes single actor.
    - Returns the deleted actor data.

- Sample:`curl -H "Authorization: $CASTING_PRODUCER_JWT" http://127.0.0.1:5000/actors/9 -X DELETE`

```json
{
  "actor": {
    "age": 66, 
    "gender": "F", 
    "id": 9, 
    "name": "Soad Hosny"
  }, 
  "success": true
}
```

##### PATCH /actors/\<int:actor_id>

- General:
    - Update actor data.
    - Returns the updated actor data.

- Sample:`curl -H "Authorization: $CASTING_PRODUCER_JWT" -H "Content-Type: application/json" -d '{"name": "miena shalaby","age":45,"gender":"F"}'  http://127.0.0.1:5000/actors/2 -X PATCH`

```json
{
  "actor": {
    "age": 45, 
    "gender": "F", 
    "id": 2, 
    "name": "miena shalaby"
  }, 
  "success": true
}
```

##### POST /actors

- General:
    - Adds a new actor.
    - Returns the added actor data.

- Sample:`curl -H "Authorization: $CASTING_PRODUCER_JWT" -H "Content-Type: application/json" -d '{"name": "Sandra Bolack","age":50,"gender":"F"}'  http://127.0.0.1:5000/actors -X POST`


```json
{
  "actor": {
    "age": 50, 
    "gender": "F", 
    "id": 10, 
    "name": "Sandra Bolack"
  }, 
  "success": true
}

```



## Authors
Rafy amgad benjamin is the author of APIs and all the files in the structure of this application.

This application is part of [Udacity](https://www.udacity.com/) in full stack development track in Nanodegree.


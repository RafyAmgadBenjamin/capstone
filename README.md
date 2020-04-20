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
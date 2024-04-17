# Movie API Documentation

This API allows users to perform various operations related to movies such as registration, login, movie creation, listing all movies, and searching for movies based on different parameters like title, genre, director, year, and keywords.

### Case 1: If you have docker installed, then run these following commands :-

    - docker compose build
    - docker compose up

### Case 2: Computer: Local Enviornment Setup

    1. Create and Enter virtual enviorment
          virtualenv env
          source env/bin/activate

    2. Install all dependencies
          pip3 install -r requirements.txt

    3. Setup Models
          python3 manage.py makemigrations
          python3 manage.py migrate

    4. Run server
          python3 manage.py runserver


## Base URL

```
http://127.0.0.1:8000/api/
```

## Endpoints

### 1. User Registration

- URL: /register/
- Method: POST
- Description: Registers a new user.
- Request Body:
  ```json
  {
      "username": "example_user",
      "password": "password123",
      "email": "user@example.com",
      "phone": "1234567890",
      "first_name": "John",
      "last_name": "Doe"
  }
  ```
- curl : 
  ```
  curl -X POST \
  http://127.0.0.1:8000/api/register/ \
  -H 'Content-Type: application/json' \
  -d '{
      "username": "example_user",
      "password": "password123",
      "email": "user@example.com",
      "phone": "1234567890",
      "first_name": "John",
      "last_name": "Doe"
  }'
  ```

- Response:
  ```json
  {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
  }
  ```

### 2. User Login

- URL: /login/
- Method: POST
- Description: Logs in an existing user.
- Request Body:
  ```json
  {
      "username": "example_user",
      "password": "password123"
  }
  ```
  
- Curl :
  ```
  curl -X POST \
  http://127.0.0.1:8000/api/login/ \
  -H 'Content-Type: application/json' \
  -d '{
      "username": "example_user",
      "password": "password123"
  }'

  ```

- Response:
  ```json
  {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
  }
  ```

### 3. Token Refresh

- URL: /refresh/
- Method: POST
- Description: Refreshes the access token.
- Request Body:
  ```json
  {
      "refresh": "<refresh_token>"
  }
  ```

- Curl :
  ```
  curl -X POST \
  http://127.0.0.1:8000/api/refresh/ \
  -H 'Content-Type: application/json' \
  -d '{
      "refresh": "<refresh_token>"
  }'
  ```

  
- Response:

  ```json
  {
      "access": "<new_access_token>"
  }
  ```

### 4. Movie Creation

- URL: /movies/
- Method: POST
- Description: Creates a new movie entry.
- Authorization: Bearer Token (Access Token)
- Request Body:
  ```json
  {
      "title": "Movie Title",
      "runtime": "120 min",
      "year": "2023",
      "directors": ["name1", "name2"],
      "genres": ["type1", "type2"]
  }
  ```
- Curl :
  ```
  curl -X POST \
  http://127.0.0.1:8000/api/movies/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{
      "title": "Movie Title",
      "runtime": "120 min",
      "year": "2023",
      "directors": ["name1", "name2"],
      "genres": ["type1", "type2"]
  }'
  ```
  
- Response:
  ```json
  {
      "id": 1,
      "title": "Movie Title",
      "runtime": "120 min",
      "year": "2023",
      "directors": ["Director 1", "Director 2"],
      "genres": ["Genre 1", "Genre 3"]
  }
  ```

### 5. List All Movies

- URL: /movieslist/
- Method: GET
- Description: Retrieves a list of all movies.
- Authorization: Bearer Token (Access Token)
- Response: List of movie objects.

- Curl :
  ```
  curl -X GET \
  http://127.0.0.1:8000/api/movieslist/ \
  -H 'Authorization: Bearer <access_token>'

  ```

### 6. Movie Search

- URL: /search/
- Method: POST
- Description: Searches for movies based on provided parameters.
- Authorization: Bearer Token (Access Token)
- Request Body:
  ```json
  {
      "title": "Movie Title",
      "genre": "Action",
      "director": "Director Name",
      "year": "2023",
      "keyword": "Keyword"
  }
  ```
- Curl :
  ```
  curl -X POST \
  http://127.0.0.1:8000/api/search/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <access_token>' \
  -d '{
      "title": "Movie Title",
      "genre": "Action",
      "director": "Director Name",
      "year": "2023",
      "keyword": "Keyword"
  }'

  ```

- Response: List of movie objects matching the search criteria.

## Query Parameters for Movie Search

- title (optional): Search movies by title.
- genre (optional): Filter movies by genre.
- director (optional): Filter movies by director name.
- year (optional): Filter movies by release year.
- keyword (optional): Search movies by a keyword in the title.

## Example Request

```http
POST /api/search/
Content-Type: application/json
Authorization: Bearer <access_token>

{
    "title": "Avengers",
    "genre": "Action"
}
```
- Curl :
 ```
    curl -X POST \
    http://127.0.0.1:8000/api/search/ \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer <access_token>' \
    -d '{
        "title": "Movie Title",
        "genre": "Action",
        "director": "Director Name",
        "year": "2023",
        "keyword": "Keyword"
    }'
 ```

## Example Response

```json
[
    {
        "id": 1,
        "title": "Avengers: Endgame",
        "runtime": "181 min",
        "year": "2019",
        "directors": ["Anthony Russo", "Joe Russo"],
        "genres": ["Action", "Adventure"]
    },
    {
        "id": 2,
        "title": "Avengers: Infinity War",
        "runtime": "149 min",
        "year": "2018",
        "directors": ["Anthony Russo", "Joe Russo"],
        "genres": ["Action", "Adventure"]
    }
]
```


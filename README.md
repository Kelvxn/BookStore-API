## Introduction
A book store API. An API where users can view books they want to buy or add it to their bookmark for later, view & subscribe to publishers and/or authors to get notified by email when the publisher/author releases a new
book

Built with Django & Django Rest Framework.


## API Endpoints 
### API Root
Get a list of available API endpoints
```
http://localhost:8000/api/ - GET
```

### Authentication
Register account
```
http://localhost:8000/api/accounts/ - POST

Body:
    "username": "djangonaut",
    "first_name": "django",
    "last_name": "user",
    "email": "djangouser@dj.com",
    "password": "12345",
    "password2": "12345",
```

Login to user account
```
http://localhost:8000/api-auth/login/ - POST

Body: 
    "username": "djangonaut",
    "password": "12345",
```

### Book
View a list of all books
```
http://localhost:8000/api/books/ - GET
```

Create a book object - (Admin)
```
http://localhost:8000/api/books/ - POST
```

View a single book object
```
http://localhost:8000/api/books/{id}/ - GET
```

Add a book object to bookmark
```
http://localhost:8000/api/books/{id}/bookmark/ - POST
```

Update a book object - (Admin)
```
http://localhost:8000/api/books/{id}/ - PUT
```

Delete a book object - (Admin)
```
http://localhost:8000/api/books/{id}/ - DELETE
```

### Author
View a list of all authors and books written
```
http://localhost:8000/api/authors/ - GET
```

Create an author object - (Admin)
```
http://localhost:8000/api/authors/ - POST
```

View a single author object
```
http://localhost:8000/api/authors/{slug}/ - GET
```

Update an author object - (Admin)
```
http://localhost:8000/api/authors/{slug}/ - PUT
```

Delete an author object - (Admin)
```
http://localhost:8000/api/authors/{slug}/ - DELETE
```

### Publisher
View a list of all publishers and books published.
```
http://localhost:8000/api/publishers/ - GET
```

Create a publisher object - (Admin)
```
http://localhost:8000/api/publishers/ - POST
```

View a single publisher object
```
http://localhost:8000/api/publishers/{slug}/ - GET
```

Subscribe to a publisher 
```
http://localhost:8000/api/publishers/{slug}/subscribe/ - POST
```

Update a publisher object - (Admin)
```
http://localhost:8000/api/publishers/{slug}/ - PUT
```

Delete a publisher object - (Admin)
```
http://localhost:8000/api/publishers/{slug}/ - DELETE
```


## Cloning the repository 
```
git clone https://github.com/Kelvxn/BookStore-API
```

Open to PR and suggestions/questions :)

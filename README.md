## Introduction
A book store API. An API where users can view books they want to buy or add it to their bookmark for later, view & subscribe to publishers to get notified by email when a publisher publishes a new book and also, view authors to see list of books they've written.

Built with Django & Django Rest Framework.


## API Endpoints 
### API Root
Get a list of available API endpoints
```
http://localhost:8000/api/ - GET
```

### Authentication
Register a user
```
http://localhost:8000/api/accounts/ - POST
```

Login to user account
```
http://localhost:8000/api-auth/login/ - POST
```

### Book
View a list of all books
```
http://localhost:8000/api/books/ - GET
```

Create a book object - (Admin users)
```
http://localhost:8000/api/books/ - POST
```

View a single book object
```
http://localhost:8000/api/books/{id}/ - GET
```

Add a book object to bookmark - (Authenticated Users)
```
http://localhost:8000/api/books/{id}/bookmark/ - POST
```

Update a book object - (Admin users)
```
http://localhost:8000/api/books/{id}/ - PUT
```

Delete a book object - (Admin users)
```
http://localhost:8000/api/books/{id}/ - DELETE
```

### Author
View a list of all authors and books written
```
http://localhost:8000/api/authors/ - GET
```

Create an author object - (Admin users)
```
http://localhost:8000/api/authors/ - POST
```

View a single author object
```
http://localhost:8000/api/authors/{slug}/ - GET
```

Update an author object - (Admin users)
```
http://localhost:8000/api/authors/{slug}/ - PUT
```

Delete an author object - (Admin users)
```
http://localhost:8000/api/authors/{slug}/ - DELETE
```

### Publisher
View a list of all publishers and books published.
```
http://localhost:8000/api/publishers/ - GET
```

Create a publisher object - (Admin users)
```
http://localhost:8000/api/publishers/ - POST
```

View a single publisher object
```
http://localhost:8000/api/publishers/{slug}/ - GET
```

Subscribe to a publisher  - (Authenticated Users)
```
http://localhost:8000/api/publishers/{slug}/subscribe/ - POST
```

Update a publisher object - (Admin users)
```
http://localhost:8000/api/publishers/{slug}/ - PUT
```

Delete a publisher object - (Admin users)
```
http://localhost:8000/api/publishers/{slug}/ - DELETE
```


## Cloning the repository 
```
git clone https://github.com/Kelvxn/BookStore-API
```

Open to PR and suggestions/questions :)

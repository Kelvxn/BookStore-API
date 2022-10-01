## Introduction
A book store API. An API where users can view books they want to buy or add it to thier bookmark for later, view & subscribe to publishers to get notified by email when a publisher publishes a new book and also, view authors to see list of books they've written.

## API Endpoints 
API Root
    /api/ - GET
    Get a list of available API endpoints

Authentication
    /api/accounts/ - POST
    Register a user

    /api-auth/ - POST
    Login to user account

Books
    /api/books/ - GET
    View a list of all books

    /api/books/ - POST
    Create a book object - (Admin users)

    /api/books/<uuid:pk>/ - GET
    View a single book object

    /api/books/<uuid:pk>/bookmark/ - POST
    Add a book object to bookmark - (Authenticated Users)

    /api/books/<uuid:pk>/ - PUT
    Update a book object - (Admin users)

    /api/books/<uuid:pk>/ - DELETE
    Delete a book object - (Admin users)

Authors
    /api/authors/ - GET
    View a list of all authors and books written

    /api/authors/ - POST
    Create an author object - (Admin users)

    /api/authors/<slug:slug>/ - GET
    View a single author object

    /api/authors/<slug:slug>/ - PUT
    Update an author object - (Admin users)

    /api/authors/<slug:slug>/ - DELETE
    Delete an author object - (Admin users)

Publishers
    /api/publishers/ - GET
    View a list of all publishers and books published.

    /api/publishers/ - POST
    Create a publisher object - (Admin users)

    /api/publishers/<slug:slug> - GET
    View a single publisher object

    /api/publishers/<slug:slug>/subscribe/ - POST
    Subscribe to a publisher  - (Authenticated Users)

    /api/publishers/<slug:slug> - PUT
    Update a publisher object - (Admin users)

    /api/publishers/<slug:slug> - DELETE
    Delete a publisher object - (Admin users)


## Cloning the repository 
```
git clone https://github.com/Kelvxn/BookStore-API
```

Open to PR and suggestions/questions :)
# Address Book Server

## Description

This is a server to the [Address Book Client](https://github.com/r-giskard-reventlov/address_book_client "Address Book Client").

This application demonstrates the usage of a Python service which exposes a RESTful API allowing for organisation and
their personel to be managed.

## Installation

Python: 3.x

This application uses Pip for dependencies so as long as you have Bower on you machine:

```
pip install -r requirements.txt
```

The server is run on `localhost:8080` so please make sure this port is unused.

## Running

To run the server call the python script run.py

```
python run.py
```

This service can be tested without the need for the client, just use your favourite REST client:

```
GET    http://localhost:8080 [discovery endpoint]

GET    http://localhost:8080/organisations [list organisations]
POST   http://localhost:8080/organisations [add organisation]

GET    http://localhost:8080/organisations/:id [an organisation identified by :id]
PUT    http://localhost:8080/organisations/:id [replace organisation]
DELETE http://localhost:8080/organisations/:id [delete the organisation]
```

This service is also designed to be Hateoas compliant.

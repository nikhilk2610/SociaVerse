# SociaVerse
A social media app with following functionality 
- Signup/Login
- Authentication
- Searching user by name or email id
- sending/accepting/rejecting friend requests
- To get the list of friends
- To Get the list of pending friend requests

## Getting Started
Follow these instructions to set up and run the project on your local machine.

## Prerequisites
Before running the app, you need to have the following installed:

Python (version 3.7 or higher)
Django (version 3.2 or higher)
Django REST Framework (version 3.12 or higher)
djangorestframework-simplejwt (version 4.8 or higher)


## Installation
Clone the repository or download the project files.

run `git clone https://github.com/nikhilk2610/SociaVerse.git`

run `cd socia_app`

run `pip install -r requirements.txt`

### Database Setup
By default, the app uses the SQLite database. You can change the database settings in the settings.py file if needed.

### Run migrations to create the database tables.
`python manage.py migrate`

## Running the App
Use the following command to start the development server:
`python manage.py runserver`


The app will be accessible at http://127.0.0.1:8000/ or http://localhost:8000/.

## API Endpoints
The following API endpoints are available in this app:

### To register user/Signup:
POST `/api/signup/`: For Registration of the user.

Request payload:
```
{
    "email": "nikhil@gmail.com",
    "name": "Nikhil",
    "password": "Nikhil@1"
}
```

### Login:
POST `/api/login/`: Get a JWT token by providing valid credentials. This endpoint uses TokenObtainPairView. The access token will be used in every api call will be passed in headers.

Request payload:
```
{
    "email": "nikhil@gmail.com",
    "password": "Nikhil@1"
}
```

Response:
```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMjYxNjA3LCJpYXQiOjE2OTA5MDE2MDcsImp0aSI6ImQ0NGYwNjQwNmIwMDQzZDhiNWFhMzA2M2U3N2IzY2VhIiwidXNlcl9pZCI6NH0.1AzuX_TQOG3nyuOxX3EDaofLz_HgZ-Ojs6VZqWj8Icc",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDk4ODAwNywiaWF0IjoxNjkwOTAxNjA3LCJqdGkiOiI4MDdhMGRkNTQ5YTc0MTk5OTkyY2E4NDU2MDAxZDAwOSIsInVzZXJfaWQiOjR9.ZtUXLHKa7a6A8dMAJa2KdwW1CXEKOVzHt6-_6Q5i3MQ"
}
```

This access_token will be passed in every api call as:
Request Headers:
````
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMjYxNjA3LCJpYXQiOjE2OTA5MDE2MDcsImp0aSI6ImQ0NGYwNjQwNmIwMDQzZDhiNWFhMzA2M2U3N2IzY2VhIiwidXNlcl9pZCI6NH0.1AzuX_TQOG3nyuOxX3EDaofLz_HgZ-Ojs6VZqWj8Icc
````


### User Search
GET `/api/search/`: Get a list of user based on provided name or email.
Request: `/search/?query=nik` or `/search/?query=nikhil@gmail.com`
Response: 
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "nikhil@gmail.com",
            "name": "Nikhil"
        }
    ]
}
```

### To send friend requests:
POST `/api/friend-requests/`: To send the friend requests to the other users.

Request payload:
```
{
    "receiver_id": 2
}
```
Response:
````
{
    "sender": 1,
    "receiver": 2,
    "status": "pending",
    "created_at": "2023-08-01T16:10:31.569808Z"
}
````

### To accept/reject friend request:
PUT, PATCH `/api/friend-requests/action/`: To accept/reject the friend requests from the other users.

Request payload:
```
{
    "sender_id": 1,
    "action": "accept"
}
```
Response:
````
{
    "sender": 1,
    "receiver": 2,
    "status": "accepted",
    "created_at": "2023-08-01T14:20:23.794547Z"
}
````

### To get the list of all friends:
GET `/api/friends/`: To see the list of all friends who has accepted the request.
Request: `/api/friends/` with token in headers
Response:
````
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "email": "nakul@gmail.com",
            "name": "Nakul Dev"
        }
    ]
}
````

### To get the list of all pending friend requests:
GET `/api/pending-friend-requests/`: To see the list of all pending friend requests from other users.
Request: `/api/pending-friend-requests/` with token in headers
Response:
````
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "sender": 3,
            "receiver": 1,
            "status": "pending",
            "created_at": "2023-08-01T14:49:43.594346Z"
        }
    ]
}
````

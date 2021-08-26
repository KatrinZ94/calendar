# Application CALENDAR

## Application Tasks

* scheduling custom events
* tracking public holidays


## Get Started (requirements: Docker)

* copy project from GitHub
* run cmd from root folder (folder with files Dockerfile and docker-compose.yml)
* enter command: doker-compose up

## EndPoints

### 1. Registration and creating a profile:
 ```sh
/user/registration/
```
###### Allow methods: POST, OPTIONS
Request (POST-method)
 
 ```
{
    "email": "email@email.email",
    "username": "Nickname",
    "password": "password",
    "profile": {
        "phone": "+375291111111",
        "first_name": "Name",
        "Last_name": "Surname",
        "birth_date": "2021-08-26",
        "gender": "f",
        "country": 19
    }
}
```
Response:

```
{
    "email": "email@email.email",
    "username": "Nickname",
    "password": "pbkdf2_sha256$260000$E4iRJbetgAlx3I6oC1bdpi$Staa9GBvDLeiF3tBDKKiKBOIRvNA0Ol79ggHFV79ll4=",
    "profile": {
        "id": 3,
        "phone": "+375291111111",
        "first_name": "Name",
        "Last_name": "Surname",
        "birth_date": "2021-08-26",
        "gender": "f",
        "country": 19
    }
}
```
_You will receive an email with an activator link_
    
### 2. Getting token:
 ```sh
/user/api/token/
```
###### Allow methods: POST, OPTIONS
Request (POST-method)
``` 
{
    "username": "katrin.z.94@mail.ru",
    "password": "arccos90"
}
```
Response:

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTk4MDczOSwianRpIjoiYjYwNWEyMGJmM2I5NDgzM2FlODhjOTI4NDBiZDM4MTciLCJ1c2VyX2lkIjoxfQ.mNCwPaX9LuRKZRi5T4Zvtf0FTA3net1VBZnM2-oX7es",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5ODk0NjM5LCJqdGkiOiIwNmI4Y2JkY2M2Nzg0M2FjYTUyYjY0M2YzMWY1NWUwZCIsInVzZXJfaWQiOjF9.rIXj7uqvErD49gJKc1M6LXsoHLhT55PTZkMe-31Pma4"
}
```
_For all of the following requests insert the token into the request header, for example: headers = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5ODk0NjM5LCJqdGkiOiIwNmI4Y2JkY2M2Nzg0M2FjYTUyYjY0M2YzMWY1NWUwZCIsInVzZXJfaWQiOjF9.rIXj7uqvErD49gJKc1M6LXsoHLhT55PTZkMe-31Pma4"}
k_

### 3. User profile editing (Viewin User profile):
 ```sh
/user/profile_edit/
```
###### Allow methods: GET, PUT, PATCH, HEAD, OPTIONS
Request (PUT-method)
 
 ```
{
    "phone": "+375291111112",
    "first_name": "Name2",
    "Last_name": "Surname2",
    "birth_date": "2021-08-26",
    "gender": "f",
    "country": 19
}
```
Response:

```
{
    "id": 3,
    "phone": "+375291111112",
    "first_name": "Name2",
    "Last_name": "Surname2",
    "birth_date": "2021-08-26",
    "gender": "f",
    "country": 19
}
```
### 4. Create event:
 ```sh
/event/create_event/
```
###### Allow methods: POST, OPTIONS
Request (POST-method)
 
 ```
{
    "name": "Событие 1",
    "start_date": "2021-08-26T20:00:00.000000+03:00",
	"end_date": "2021-08-26T21:00:00.000000+03:00"
    "reminder_before": 1
}
```
- "name" - enter event name (required field) 
- "start_date" - enter event name, date and start time of event (required field)
- "end_date" - enter time end of event (default = "23:59:59")
- "reminder_before" - if you need to receive a reminder email, enter the number of hours before the event starts 

##### Possible values:

|  |  |
| ------ | ------ |
| 1 | hour |
| 2 | 2 hours |
| 4 | 4 hours |
| 24 | day |
| 168 | week |

Response:

```
{
    "id": 146,
    "name": "Событие 1",
    "start_date": "2021-08-26T17:00:00Z",
    "end_date": "2021-08-26T21:00:00.00Z",
    "reminder_before": 1
}
```
### 5. Editing an event:
 ```sh
/event/event/<int:id_event>
```
###### Allow methods: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Request (PUT-method)

###### exemple:  
```/event/event/146```
 
 ```
{
    "name": "Событие отредактировано 1",
    "start_date": "2021-09-01T09:00:00.000000+03:00",
    "end_date": "2021-09-01T10:00:00.000000+03:00",
    "reminder_before": 2
}
```
Response:

```
{
    "id": 146,
    "name": "Событие отредактировано 1",
    "start_date": "2021-09-01T09:00:00Z",
    "end_date": "2021-09-01T10:00:00.00Z",
    "reminder_before": 2
}
```
### 6. Getting a list of all events of a specific user:
 ```sh
/event/all_events/
```
###### Allow methods: GET, HEAD, OPTIONS
Request (GET-method)

Response:

```

    [
    {
        "id": 146,
        "name": "Событие отредактировано 11",
        "start_date": "2021-09-01T06:00:00Z",
        "end_date": "2021-09-01T07:00:00Z",
        "reminder_before": 2
    },
    {
        "id": 147,
        "name": "Событие 2",
        "start_date": "2021-08-27T17:00:00Z",
        "end_date": "2021-08-27T23:59:59.999999Z",
        "reminder_before": 1
    },
    {
       ...
    },
    {
      ...
    }
]
```

### 7. Getting a list of events for the day of a specific user:
 ```sh
event/events_of_day/<int:day>/<int:month>/<int:year>
```
###### Allow methods: GET, HEAD, OPTIONS
Request (GET-method with params)

###### exemple:  
```/event/events_of_day/01/09/2021```
 

Response:

```
[
    {
        "name": "Событие отредактировано 11",
        "start_date": "2021-09-01T06:00:00Z"
    },
    {
        "name": "Событие 4",
        "start_date": "2021-09-01T17:00:00Z"
    },
    {
       ...
    },
    {
      ...
    },
    {
      ...
    }
]
```

### 8. Getting the general aggregation of events by day for the month:
 ```sh
event/events_of_month/<int:month>/<int:year>
```
###### Allow methods: GET, HEAD, OPTIONS
Request (GET-method with params)

###### exemple:  
```/event/events_of_month/09/2021```
 

Response:

```
[
    {
        "date": "2021-09-01",
        "events": [
            {
                "name": "Событие отредактировано 11",
                "start_date": "2021-09-01T06:00:00Z"
            },
            {
                "name": "Событие 4",
                "start_date": "2021-09-01T17:00:00Z"
            },
            {
                "name": "Событие 5",
                "start_date": "2021-09-01T18:00:00Z"
            },
            {
                "name": "Событие 6",
                "start_date": "2021-09-01T06:00:00Z"
            },
            {
                "name": "Событие отредактировано 7",
                "start_date": "2021-09-01T07:00:00Z"
            },
            {
                "name": "Событие 7",
                "start_date": "2021-09-01T06:00:00Z"
            },
        ]
    },
    {
        "date": "2021-09-02",
        "events": []
    },
    {
        "date": "2021-09-03",
        "events": []
    },
    {
        "date": "2021-09-04",
        "events": []
    },
    
    ...
    
    {
        "date": "2021-09-30",
        "events": []
    }
]
```

### 8. Getting a list of Public Holidays for the month:
 ```sh
event/public_holiday/<int:month>/<int:year>
```
###### Allow methods: GET, HEAD, OPTIONS
Request (GET-method with params)

###### exemple:  
```/event/public_holiday/01/2022```
 

Response:

```
[
    {
        "name": "Belarus: Orthodox Christmas",
        "start_date": "2022-01-07T00:00:00Z"
    },
    {
        "name": "Belarus: Day after New Year's Day",
        "start_date": "2022-01-02T00:00:00Z"
    },
    {
        "name": "Belarus: New Year's Day",
        "start_date": "2022-01-01T00:00:00Z"
    }
]
```
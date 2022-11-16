# Endpoints documentation

## User Routes

### /users/
* Description: get all users
* Method: GET
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only 
* Request body: None
* Response body

```py
[
    {
        "id": 1,
        "f_name": "Rachel",
        "l_name": "Green",
        "phone": "300573",
        "personal_email": "rachel.green@friends.com",
        "type": {
            "name": "Client"
        }
    }
]
```

### /users/user_id
* Description: get one user 
* Method: GET
* Argument: user_id as Integer
* Authentication: jwt bearer token 
* Authorization: employees only 
* Request body: None
* Response body

```py
{
    "id": 1,
    "f_name": "Rachel",
    "l_name": "Green",
    "phone": "300573",
    "personal_email": "rachel.green@friends.com",
    "type": {
        "name": "Client"
    }
}
```

### /users/search/
* Description: search one user by phone number using query parameter
* Method: GET
* Argument: seach?phone=<phonenumber>
* Authentication: jwt bearer token 
* Authorization: employees only 
* Request body: None
* Response body

```py
{
    "id": 10,
    "f_name": "Dwight",
    "l_name": "Schrute",
    "phone": "975150",
    "personal_email": null,
    "type": {
        "name": "Employee"
    }
}
```

## Client Routes

### /clients/
* Description: get all clients
* Method: GET
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only 
* Request body: None
* Response body

```py
[
    {
        "id": 1,
        "user": {
            "f_name": "Rachel",
            "l_name": "Green",
            "phone": "300573",
            "personal_email": "rachel.green@friends.com",
            "type": {
                "name": "Client"
            }
        },
        "pets": []
    }
]
```

### /clients/client_id
* Description: get one client by id
* Method: GET
* Argument: client_id as Integer
* Authentication: jwt bearer token 
* Authorization: employees or the account owner
* Request body: None
* Response body

```py
{
    "id": 2,
    "user": {
        "f_name": "Phoebe",
        "l_name": "Buffay",
        "phone": "779149",
        "personal_email": "phoebe.buffay@friends.com",
        "type": {
            "name": "Client"
        }
    },
    "pets": []
}
```

### /clients/search/
* Description: search one client by phone number using query parameter
* Method: GET
* Argument: seach?phone=<phonenumber>
* Authentication: jwt bearer token 
* Authorization: employees and the account owner
* Request body: None
* Response body

```py
{
    "id": 4,
    "user": {
        "f_name": "Chandler",
        "l_name": "Bing",
        "phone": "871413",
        "personal_email": "chandler.bing@friends.com",
        "type": {
            "name": "Client"
        }
    },
    "pets": [
        {
            "id": 1,
            "name": "Donald",
            "breed": "Unknown",
            "year": 2022,
            "type": {
                "name": "Duck"
            },
            "size": {
                "name": "XS"
            },
            "bookings": [
                {
                    "id": 1,
                    "pet_id": 1,
                    "service_id": 1,
                    "status": "Pending",
                    "service": {
                        "name": "Full Groom",
                        "duration": 2.0,
                        "price": 150.0
                    },
                    "date": "2022-12-11",
                    "time": "10:00:00",
                    "employee": {
                        "user": {
                            "id": 10,
                            "f_name": "Dwight",
                            "l_name": "Schrute",
                            "phone": "975150",
                            "personal_email": null,
                            "type": {
                                "name": "Employee"
                            }
                        }
                    },
                    "date_created": "2022-11-12"
                }
            ],
            "type_id": 5,
            "size_id": 1,
            "client_id": 4
        }
```

### /clients/
* Description: create a new client (onsite)
* Method: POST
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only 
* Request body: 
    * required: l_name, f_name, phone
    * optional: personal_email, password

```py
{
    "f_name": "Mighty",
    "l_name": "Minion",
    "phone": "300577",
    "personal_email": "minion_loves_dogs@spam.com"
}
```

* Request validations: 
  * f_name and l_name are longer than 2 characters
  * phone number must be unique
  * password if provided, must be longer than 6 characters, contain an uppercase character, a lowercase character, a number and a special character

* Response body:

```py
{
    "id": 16,
    "user": {
        "f_name": "Mighty",
        "l_name": "Minion",
        "phone": "300587",
        "personal_email": "minion_loves_dogs@spam.com",
        "type": {
            "name": "Client"
        }
    }
}
```

### /clients/client_id
* Description: delete one client by client_id
* Method: DELETE
* Argument: client_id as Integer
* Authentication: jwt bearer token 
* Authorization: employees or the account owner
* Request body: None
* Response body

```py
{
    "message": "Client deleted successfully"
}
```

### /clients/client_id
* Description: update one client's info by client_id
* Method: PUT, PATCH
* Argument: client_id as Integer
* Authentication: jwt bearer token 
* Authorization: employees or the account owner
* Request body: 
  * optional fields: f_name, l_name, phone, personal_email, password

```py
{
    "f_name": "Cruella",
    "phone": "391067"
}
```
* Request validations: silimar to create new client
* Response body:

```py
{
    "id": 2,
    "user": {
        "f_name": "Cruella",
        "l_name": "Buffay",
        "phone": "391067",
        "personal_email": "phoebe.buffay@friends.com",
        "type": {
            "name": "Client"
        }
    },
    "pets": []
}
```

## Employee Routes

### /employees/
* Description: get all employees
* Method: GET
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only
* Request body: None
* Response body

```py
[
    {
        "id": 10,
        "user": {
            "id": 10,
            "f_name": "Dwight",
            "l_name": "Schrute",
            "phone": "975150",
            "personal_email": null,
            "type": {
                "name": "Employee"
            }
        },
        "email": "dwight.schrute@dogspa.com",
        "is_admin": "False"
    },
    {
        "id": 11,
        "user": {
            "id": 11,
            "f_name": "Michael",
            "l_name": "Scott",
            "phone": "657403",
            "personal_email": null,
            "type": {
                "name": "Employee"
            }
        },
        "email": "michael.scott@dogspa.com",
        "is_admin": "False"
    }
]
```

### /employees/employee_id
* Description: get one employee by employee_id
* Method: GET
* Argument: employee_id
* Authentication: jwt bearer token 
* Authorization: admin and account owner only
* Request body: None
* Response body

```py
{
    "id": 11,
    "user": {
        "id": 11,
        "f_name": "Michael",
        "l_name": "Scott",
        "phone": "657403",
        "personal_email": null,
        "type": {
            "name": "Employee"
        }
    },
    "email": "michael.scott@dogspa.com",
    "is_admin": "False"
}
```

### /employees/search/
* Description: search one employee by phone number using query parameter
* Method: GET
* Argument: search?phone=phonenumber
* Authentication: jwt bearer token 
* Authorization: admin and account owner only
* Request body: None
* Response body

```py
{
    "id": 11,
    "user": {
        "id": 11,
        "f_name": "Michael",
        "l_name": "Scott",
        "phone": "657403",
        "personal_email": null,
        "type": {
            "name": "Employee"
        }
    },
    "email": "michael.scott@dogspa.com",
    "is_admin": "False"
}
```

### /employees/employee_id
* Description: delete one employee by employee_id
* Method: DELETE
* Argument: employee_id
* Authentication: jwt bearer token 
* Authorization: admin only
* Request body: None
* Response body

```py
{
    "message": "Employee deleted successfully"
}
```

### /employees/
* Description: create a new employee
* Method: POST
* Argument: None
* Authentication: jwt bearer token 
* Authorization: admin only
* Request body: 
    * required: l_name, f_name, phone
    * optional: personal_email, is_admin

```py
{
    "f_name": "Samuel",
    "l_name": "Smith",
    "phone": "023539",
    "is_admin": "true"
}
```

* Request validations: 
  * f_name and l_name are longer than 2 characters
  * phone number must be unique
  * is_admin must be either true or false

* Response body:

```py
{
    "id": 25,
    "user": {
        "id": 25,
        "f_name": "Samuel",
        "l_name": "Smith",
        "phone": "023539",
        "personal_email": null,
        "type": {
            "name": "Employee"
        }
    },
    "email": "samuel.smith@dog_spa.com",
    "is_admin": "True"
}
```

### /employees/employee_id
* Description: edit employee's info using employee_id
* Method: PUT, PATCH
* Argument: employee_id
* Authentication: jwt bearer token 
* Authorization: admin and account owner only
* Request body: 
    * optional: f_name, l_name, phone, password, personal_email, email, is_admin

```py
{
    "f_name": "Minion",
    "password": "Scotty12#",
    "personal_email": "scotty_loves_dogs@spam.com", 
    "is_admin": "true"
}
```

* Request validations: 
  * f_name and l_name are longer than 2 characters
  * phone number must be unique
  * is_admin must be either true or false. Only admin can edit this field.
  * Only admin can edit email
  * password must be longer than 6 characters, contain an uppercase character, a lowercase character, a number and a special character

* Response body:

```py
{
    "id": 11,
    "user": {
        "id": 11,
        "f_name": "Minion",
        "l_name": "Scott",
        "phone": "657403",
        "personal_email": "scotty_loves_dogs@spam.com",
        "type": {
            "name": "Employee"
        }
    },
    "email": "michael.scott@dogspa.com",
    "is_admin": "True"
}
```

## Authentication Routes

### /auth/register
* Description: register new client (online)
* Method: POST
* Argument: None
* Authentication: None
* Authorization: None
* Request body: 
  * required fields: f_name, l_name, phone, password, personal_email
```py
{
    "f_name": "My name",
    "l_name": "Last",
    "personal_email": "someone@spam.com",
    "phone": "891413",
    "password": "Someone123?"
}
```
* Request validations:
  * f_name and l_name are longer than 2 characters
  * phone number must be unique
  * password must be longer than 6 characters, contain an uppercase character, a lowercase character, a number and a special character

* Response body
```py
{
    "id": 27,
    "user": {
        "f_name": "My name",
        "l_name": "Last",
        "phone": "891413",
        "personal_email": "someone@spam.com",
        "type": {
            "name": "Client"
        }
    }
}
``` 
### /auth/login/
* Description: login
* Method: POST
* Argument: None
* Authentication: None
* Authorization: None
* Request body: 
```py
{
    "email": "admin@dogspa.com",
    "password": "Admin123!"
}
```
* Response body:
```py
{
    "email": "admin@dogspa.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODMxNDM0NSwianRpIjoiZDExOWJlNmMtZWEwZS00YjM2LWFmZmUtNjhhY2M3NGVlMDQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTQsIm5iZiI6MTY2ODMxNDM0NSwiZXhwIjoxNjY4NDAwNzQ1fQ.-72BiNORWvXVwJl8NXXOiOUz_8mhReeQfXIHWX4uh2k",
    "is_admin": true
}
```

## Pet Routes

### /pets/
* Description: get all pets
* Method: GET
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only
* Request body: None
* Response body

```py
[
    {
        "id": 1,
        "name": "Donald",
        "breed": "Unknown",
        "year": 2022,
        "type": {
            "name": "Duck"
        },
        "size": {
            "name": "XS"
        },
        "client": {
            "user": {
                "f_name": "Chandler",
                "l_name": "Bing",
                "phone": "871413",
                "personal_email": "chandler.bing@friends.com",
                "type": {
                    "name": "Client"
                }
            },
            "id": 4
        },
        "bookings": [
            {
                "id": 1,
                "pet_id": 1,
                "service_id": 1,
                "status": "Pending",
                "service": {
                    "name": "Full Groom",
                    "duration": 2.0,
                    "price": 150.0
                },
                "date": "2022-12-11",
                "time": "10:00:00",
                "employee": {
                    "user": {
                        "id": 10,
                        "f_name": "Dwight",
                        "l_name": "Schrute",
                        "phone": "975150",
                        "personal_email": null,
                        "type": {
                            "name": "Employee"
                        }
                    }
                },
                "date_created": "2022-11-14"
            }
        ],
        "type_id": 5,
        "size_id": 1,
        "client_id": 4
    },
    {
        "id": 2,
        "name": "Mozzarella",
        "breed": "Cocker Spaniel",
        "year": 2019,
        "type": {
            "name": "Dog"
        },
        "size": {
            "name": "M"
        },
        "client": {
            "user": {
                "f_name": "Joey",
                "l_name": "Tribbiani",
                "phone": "271746",
                "personal_email": "joey.tribbiani@friends.com",
                "type": {
                    "name": "Client"
                }
            },
            "id": 3
        },
        "bookings": [
            {
                "id": 2,
                "pet_id": 2,
                "service_id": 2,
                "status": "Pending",
                "service": {
                    "name": "Freshen Up",
                    "duration": 1.0,
                    "price": 80.0
                },
                "date": "2022-12-18",
                "time": "13:00:00",
                "employee": {
                    "user": {
                        "id": 12,
                        "f_name": "Jim",
                        "l_name": "Halpert",
                        "phone": "349082",
                        "personal_email": null,
                        "type": {
                            "name": "Employee"
                        }
                    }
                },
                "date_created": "2022-11-14"
            }
        ],
        "type_id": 1,
        "size_id": 3,
        "client_id": 3
    }
]
```

### /pets/pet_id
* Description: get one pet by pet_id
* Method: GET
* Argument: pet_id
* Authentication: jwt bearer token 
* Authorization: employee and account owner only
* Request body: None
* Response body

```py
{
    "id": 5,
    "name": "Garfield",
    "breed": "Short-haired",
    "year": 2020,
    "type": {
        "name": "Cat"
    },
    "size": {
        "name": "S"
    },
    "client": {
        "user": {
            "f_name": "Ross",
            "l_name": "Geller",
            "phone": "702162",
            "personal_email": "ross.geller@friends.com",
            "type": {
                "name": "Client"
            }
        },
        "id": 5
    },
    "bookings": [],
    "type_id": 2,
    "size_id": 2,
    "client_id": 5
}
```

### /pets/search/
* Description: search one pet by phone number using query parameter
* Method: GET
* Argument: search?phone=phonenumber
* Authentication: jwt bearer token 
* Authorization: employee and account owner only
* Request body: None
* Response body

```py
{
    "id": 4,
    "name": "Grumpy",
    "breed": "Short-haired",
    "year": 2020,
    "type": {
        "name": "Cat"
    },
    "size": {
        "name": "S"
    },
    "client": {
        "user": {
            "f_name": "Chandler",
            "l_name": "Bing",
            "phone": "871413",
            "personal_email": "chandler.bing@friends.com",
            "type": {
                "name": "Client"
            }
        },
        "id": 4
    },
    "bookings": [
        {
            "id": 4,
            "pet_id": 4,
            "service_id": 1,
            "status": "Pending",
            "service": {
                "name": "Full Groom",
                "duration": 2.0,
                "price": 150.0
            },
            "date": "2022-12-21",
            "time": "09:00:00",
            "employee": {
                "user": {
                    "id": 13,
                    "f_name": "Cathy",
                    "l_name": "Simms",
                    "phone": "754022",
                    "personal_email": null,
                    "type": {
                        "name": "Employee"
                    }
                }
            },
            "date_created": "2022-11-14"
        }
    ],
    "type_id": 2,
    "size_id": 2,
    "client_id": 4
}
```

### /pets/pet_id
* Description: delete one pet by pet_id
* Method: DELETE
* Argument: pet_id
* Authentication: jwt bearer token 
* Authorization: admin only
* Request body: None
* Response body

```py
{
    "message": "Pet deleted successfully"
}
```

### /pets/
* Description: create a new pet
* Method: POST
* Argument: None
* Authentication: jwt bearer token 
* Authorization: None
* Request body: 
    * required: name, client_id, type_id, size_id, year
    * optional: breed

```py
{
    "name": "Marcel",
    "client_id": 4,
    "type_id": 2,
    "size_id": 1,
    "year": 2018
}
```

* Request validations: 
  * name has to be longer than 2 characters
  * a client can only create a pet with their id as client_id
  * combination of pet's name, client_id and type_id is unique

* Response body:

```py
{
    "id": 6,
    "name": "Marcel",
    "breed": "Unknown",
    "year": 2018,
    "type": {
        "name": "Cat"
    },
    "size": {
        "name": "XS"
    },
    "client": {
        "user": {
            "f_name": "Chandler",
            "l_name": "Bing",
            "phone": "871413",
            "personal_email": "chandler.bing@friends.com",
            "type": {
                "name": "Client"
            }
        },
        "id": 4
    },
    "bookings": [],
    "type_id": 2,
    "size_id": 1,
    "client_id": 4
}
```

### /pets/pet_id
* Description: edit pet's info using pet_id
* Method: PUT, PATCH
* Argument: pet_id
* Authentication: jwt bearer token 
* Authorization: employee and account owner only
* Request body: 
    * optional: name, client_id, type_id, size_id, year

```py
{
    "size_id": 1,
    "breed": "English short-haired"
}
```

* Request validations: 
  * name has to be longer than 2 characters
  * only an employee can change client_id
  * combination of pet's name, client_id and type_id is unique

* Response body:

```py
{
    "id": 4,
    "name": "Grumpy",
    "breed": "English short-haired",
    "year": 2020,
    "type": {
        "name": "Cat"
    },
    "size": {
        "name": "XS"
    },
    "client": {
        "user": {
            "f_name": "Chandler",
            "l_name": "Bing",
            "phone": "871413",
            "personal_email": "chandler.bing@friends.com",
            "type": {
                "name": "Client"
            }
        },
        "id": 4
    },
    "bookings": [
        {
            "id": 4,
            "pet_id": 4,
            "service_id": 1,
            "status": "Pending",
            "service": {
                "name": "Full Groom",
                "duration": 2.0,
                "price": 150.0
            },
            "date": "2022-12-21",
            "time": "09:00:00",
            "employee": {
                "user": {
                    "id": 13,
                    "f_name": "Cathy",
                    "l_name": "Simms",
                    "phone": "754022",
                    "personal_email": null,
                    "type": {
                        "name": "Employee"
                    }
                }
            },
            "date_created": "2022-11-14"
        }
    ],
    "type_id": 2,
    "size_id": 1,
    "client_id": 4
}
```

## Booking Routes

### /bookings/
* Description: get all bookings
* Method: GET
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees only
* Request body: None
* Response body:

```py
[
    {
        "id": 2,
        "pet_id": 2,
        "service_id": 2,
        "status": "Pending",
        "service": {
            "name": "Freshen Up",
            "duration": 1.0,
            "price": 80.0
        },
        "date": "2022-12-18",
        "time": "13:00:00",
        "pet": {
            "id": 2,
            "name": "Mozzarella",
            "breed": "Cocker Spaniel",
            "year": 2019,
            "type": {
                "name": "Dog"
            },
            "size": {
                "name": "M"
            },
            "client": {
                "user": {
                    "f_name": "Joey",
                    "l_name": "Tribbiani",
                    "phone": "271746",
                    "personal_email": "joey.tribbiani@friends.com",
                    "type": {
                        "name": "Client"
                    }
                },
                "id": 3
            },
            "type_id": 1,
            "size_id": 3,
            "client_id": 3
        },
        "employee": {
            "user": {
                "id": 12,
                "f_name": "Jim",
                "l_name": "Halpert",
                "phone": "349082",
                "personal_email": null,
                "type": {
                    "name": "Employee"
                }
            }
        },
        "date_created": "2022-11-14"
    },
    {
        "id": 3,
        "pet_id": 3,
        "service_id": 3,
        "status": "Pending",
        "service": {
            "name": "Tidy Up",
            "duration": 1.5,
            "price": 100.0
        },
        "date": "2022-12-21",
        "time": "09:00:00",
        "pet": {
            "id": 3,
            "name": "Snoopy",
            "breed": "Beagle",
            "year": 2018,
            "type": {
                "name": "Dog"
            },
            "size": {
                "name": "M"
            },
            "client": {
                "user": {
                    "f_name": "Rachel",
                    "l_name": "Green",
                    "phone": "300573",
                    "personal_email": "rachel.green@friends.com",
                    "type": {
                        "name": "Client"
                    }
                },
                "id": 1
            },
            "type_id": 1,
            "size_id": 3,
            "client_id": 1
        },
        "employee": {
            "user": {
                "id": 11,
                "f_name": "Michael",
                "l_name": "Scott",
                "phone": "657403",
                "personal_email": null,
                "type": {
                    "name": "Employee"
                }
            }
        },
        "date_created": "2022-11-14"
    }
]
```

### /bookings/booking_id
* Description: get one booking by id
* Method: GET
* Argument: booking_id
* Authentication: jwt bearer token 
* Authorization: employees and booking owner only
* Request body: None
* Response body:

```py
{
    "id": 1,
    "pet_id": 1,
    "service_id": 1,
    "status": "Pending",
    "service": {
        "name": "Full Groom",
        "duration": 2.0,
        "price": 150.0
    },
    "date": "2022-12-11",
    "time": "10:00:00",
    "pet": {
        "id": 1,
        "name": "Donald",
        "breed": "Unknown",
        "year": 2022,
        "type": {
            "name": "Duck"
        },
        "size": {
            "name": "XS"
        },
        "client": {
            "user": {
                "f_name": "Chandler",
                "l_name": "Bing",
                "phone": "871413",
                "personal_email": "chandler.bing@friends.com",
                "type": {
                    "name": "Client"
                }
            },
            "id": 4
        },
        "type_id": 5,
        "size_id": 1,
        "client_id": 4
    },
    "employee": {
        "user": {
            "id": 10,
            "f_name": "Dwight",
            "l_name": "Schrute",
            "phone": "975150",
            "personal_email": null,
            "type": {
                "name": "Employee"
            }
        }
    },
    "date_created": "2022-11-14"
}
```

### /bookings/status/booking_status
* Description: get all bookings by status
* Method: GET
* Argument: booking_status
* Authentication: jwt bearer token 
* Authorization: employees only
* Request body: None
* Response body:

```py
[
    {
        "id": 1,
        "pet_id": 1,
        "service_id": 1,
        "status": "Pending",
        "service": {
            "name": "Full Groom",
            "duration": 2.0,
            "price": 150.0
        },
        "date": "2022-12-11",
        "time": "10:00:00",
        "pet": {
            "id": 1,
            "name": "Donald",
            "breed": "Unknown",
            "year": 2022,
            "type": {
                "name": "Duck"
            },
            "size": {
                "name": "XS"
            },
            "client": {
                "user": {
                    "f_name": "Chandler",
                    "l_name": "Bing",
                    "phone": "871413",
                    "personal_email": "chandler.bing@friends.com",
                    "type": {
                        "name": "Client"
                    }
                },
                "id": 4
            },
            "type_id": 5,
            "size_id": 1,
            "client_id": 4
        },
        "employee": {
            "user": {
                "id": 10,
                "f_name": "Dwight",
                "l_name": "Schrute",
                "phone": "975150",
                "personal_email": null,
                "type": {
                    "name": "Employee"
                }
            }
        },
        "date_created": "2022-11-14"
    }
]
```

### /bookings/search/
* Description: search bookings by client's phone number using query parameter
* Method: GET
* Argument: search?phone=phonenumber
* Authentication: jwt bearer token 
* Authorization: employee and account owner only
* Request body: None
* Response body:
  
```py
{
    "id": 3,
    "user": {
        "f_name": "Joey",
        "l_name": "Tribbiani",
        "phone": "271746",
        "personal_email": "joey.tribbiani@friends.com",
        "type": {
            "name": "Client"
        }
    },
    "pets": [
        {
            "id": 2,
            "name": "Mozzarella",
            "breed": "Cocker Spaniel",
            "year": 2019,
            "type": {
                "name": "Dog"
            },
            "size": {
                "name": "M"
            },
            "bookings": [
                {
                    "id": 2,
                    "pet_id": 2,
                    "service_id": 2,
                    "status": "Pending",
                    "service": {
                        "name": "Freshen Up",
                        "duration": 1.0,
                        "price": 80.0
                    },
                    "date": "2022-12-18",
                    "time": "13:00:00",
                    "employee": {
                        "user": {
                            "id": 12,
                            "f_name": "Jim",
                            "l_name": "Halpert",
                            "phone": "349082",
                            "personal_email": null,
                            "type": {
                                "name": "Employee"
                            }
                        }
                    },
                    "date_created": "2022-11-14"
                }
            ],
            "type_id": 1,
            "size_id": 3,
            "client_id": 3
        }
    ]
}
```

### /bookings/booking_id
* Description: delete one booking by booking_id
* Method: DELETE
* Argument: booking_id
* Authentication: jwt bearer token 
* Authorization: employees or the account owner
* Request body: None
* Response body

```py
{
    "message": "Booking deleted successfully"
}
```

### /bookings/
* Description: create a new booking
* Method: POST
* Argument: None
* Authentication: jwt bearer token 
* Authorization: employees and valid users
* Request body: 
    * required: date, time, pet_id, service_id
    * optional: employee_id, status

```py
{
    "pet_id": 2, 
    "date": "2023-01-03",
    "employee_id": 10,
    "service_id": 3,
    "time": "10:05"
}
```

* Request validations: 
  * a client can only make a booking for pets they own
  * combination of pet's name, date and time is unique
  * employee_id and service_id must exist
  * date and time must be in the future

* Response body:
```py
{
    "id": 11,
    "pet_id": 2,
    "service_id": 3,
    "status": "Pending",
    "service": {
        "name": "Tidy Up",
        "duration": 1.5,
        "price": 100.0
    },
    "date": "2023-01-03",
    "time": "10:05:00",
    "pet": {
        "id": 2,
        "name": "Mozzarella",
        "breed": "Cocker Spaniel",
        "year": 2019,
        "type": {
            "name": "Dog"
        },
        "size": {
            "name": "M"
        },
        "client": {
            "user": {
                "f_name": "Joey",
                "l_name": "Tribbiani",
                "phone": "271746",
                "personal_email": "joey.tribbiani@friends.com",
                "type": {
                    "name": "Client"
                }
            },
            "id": 3
        },
        "type_id": 1,
        "size_id": 3,
        "client_id": 3
    },
    "employee_id": 10,
    "employee": {
        "user": {
            "id": 10,
            "f_name": "Dwight",
            "l_name": "Schrute",
            "phone": "975150",
            "personal_email": null,
            "type": {
                "name": "Employee"
            }
        }
    },
    "date_created": "2022-11-14"
}
```

### /bookings/booking_id
* Description: delete one booking by booking_id
* Method: DELETE
* Argument: booking_id
* Authentication: jwt bearer token 
* Authorization: employee or booking owner
* Request body: None
* Response body

```py
{
    "message": "Booking deleted successfully"
}
```

### /bookings/booking_id
* Description: edit booking's info using booking_id
* Method: PUT, PATCH
* Argument: booking_id
* Authentication: jwt bearer token 
* Authorization: employee and account owner only
* Request body: 
    * optional: pet_id, date, time, service_id, employee_id, status

```py
{
    "time": "10:15",
    "date": "2022-12-23", 
    "service_id": 3
}
```

* Request validations: 
  * only an employee can change pet_id
  * combination of pet's name, date and time is unique
  * employee_id and service_id must exist
  * date and time must be in the future

* Response body:

```py
{
    "id": 2,
    "pet_id": 2,
    "service_id": 3,
    "status": "Pending",
    "service": {
        "name": "Tidy Up",
        "duration": 1.5,
        "price": 100.0
    },
    "date": "2022-12-23",
    "time": "10:15:00",
    "pet": {
        "id": 2,
        "name": "Mozzarella",
        "breed": "Cocker Spaniel",
        "year": 2019,
        "type": {
            "name": "Dog"
        },
        "size": {
            "name": "M"
        },
        "client": {
            "user": {
                "f_name": "Joey",
                "l_name": "Tribbiani",
                "phone": "271746",
                "personal_email": "joey.tribbiani@friends.com",
                "type": {
                    "name": "Client"
                }
            },
            "id": 3
        },
        "type_id": 1,
        "size_id": 3,
        "client_id": 3
    },
    "employee_id": 12,
    "employee": {
        "user": {
            "id": 12,
            "f_name": "Jim",
            "l_name": "Halpert",
            "phone": "349082",
            "personal_email": null,
            "type": {
                "name": "Employee"
            }
        }
    },
    "date_created": "2022-11-14"
}
```

## User_types routes

### /user_types/
* Description: get all user types
* Method: GET
* Argument: None
* Authentication: jwt bearer token
* Authorization: employees only 
* Request body: None
* Response body

```py
[
    {
        "id": 1,
        "name": "Client",
        "users": [
            {
                "id": 1,
                "f_name": "Rachel",
                "l_name": "Green",
                "phone": "300573",
                "personal_email": "rachel.green@friends.com",
                "employee": {}
            },
            {
                "id": 2,
                "f_name": "Phoebe",
                "l_name": "Buffay",
                "phone": "779149",
                "personal_email": "phoebe.buffay@friends.com",
                "employee": {}
            },
            {
                "id": 3,
                "f_name": "Joey",
                "l_name": "Tribbiani",
                "phone": "271746",
                "personal_email": "joey.tribbiani@friends.com",
                "employee": {}
            },
            {
                "id": 4,
                "f_name": "Chandler",
                "l_name": "Bing",
                "phone": "871413",
                "personal_email": "chandler.bing@friends.com",
                "employee": {}
            },
            {
                "id": 5,
                "f_name": "Ross",
                "l_name": "Geller",
                "phone": "702162",
                "personal_email": "ross.geller@friends.com",
                "employee": {}
            },
            {
                "id": 6,
                "f_name": "Gunther",
                "l_name": "Adkins",
                "phone": "927623",
                "personal_email": "gunther.adkins@friends.com",
                "employee": {}
            },
            {
                "id": 7,
                "f_name": "Carol",
                "l_name": "Frye",
                "phone": "449866",
                "personal_email": "carol.frye@friends.com",
                "employee": {}
            },
            {
                "id": 8,
                "f_name": "Estelle",
                "l_name": "Leonard",
                "phone": "184288",
                "personal_email": "estelle.leonard@friends.com",
                "employee": {}
            },
            {
                "id": 9,
                "f_name": "Richard",
                "l_name": "Burke",
                "phone": "129049",
                "personal_email": "richard.burke@friends.com",
                "employee": {}
            }
        ]
    },
    {
        "id": 2,
        "name": "Employee",
        "users": [
            {
                "id": 10,
                "f_name": "Dwight",
                "l_name": "Schrute",
                "phone": "975150",
                "personal_email": null,
                "employee": {}
            },
            {
                "id": 11,
                "f_name": "Michael",
                "l_name": "Scott",
                "phone": "657403",
                "personal_email": null,
                "employee": {}
            },
            {
                "id": 12,
                "f_name": "Jim",
                "l_name": "Halpert",
                "phone": "349082",
                "personal_email": null,
                "employee": {}
            },
            {
                "id": 13,
                "f_name": "Cathy",
                "l_name": "Simms",
                "phone": "754022",
                "personal_email": null,
                "employee": {}
            },
            {
                "id": 14,
                "f_name": "admin",
                "l_name": "admin",
                "phone": "000000",
                "personal_email": null,
                "employee": {}
            }
        ]
    }
]
```

### /user_types/
* Description: create a new user type
* Method: POST
* Argument: None
* Authentication: jwt bearer token
* Authorization: admin only 
* Request body: 
  * required field: name

```py
{
    "name": "investor"
}
``` 

* Request validation:
  * name must not already exist

* Response body
  
```py
{
    "id": 3,
    "name": "Investor",
    "users": []
}
```

### /user_types/user_type.id/

* Description: get one user type by id
* Method: GET
* Argument: user_type.id
* Authentication: jwt bearer token
* Authorization: employees only
* Request body: None
* Response body:

```py
{
    "id": 1,
    "name": "Client",
    "users": [
        {
            "id": 1,
            "f_name": "Rachel",
            "l_name": "Green",
            "phone": "300573",
            "personal_email": "rachel.green@friends.com",
            "employee": {}
        },
        {
            "id": 2,
            "f_name": "Phoebe",
            "l_name": "Buffay",
            "phone": "779149",
            "personal_email": "phoebe.buffay@friends.com",
            "employee": {}
        }
    ]
}
```

### /user_types/user_type.id/

* Description: update one user type
* Method: PUT, PATCH
* Argument: user_type.id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: 
  * required: name

```py
{
    "name": "guest"
}
```

* Request validation:
  * name must not already exist

* Response body:

```py
{
    "id": 1,
    "name": "Guest",
    "users": [
        {
            "id": 1,
            "f_name": "Rachel",
            "l_name": "Green",
            "phone": "300573",
            "personal_email": "rachel.green@friends.com",
            "employee": {}
        },
        {
            "id": 2,
            "f_name": "Phoebe",
            "l_name": "Buffay",
            "phone": "779149",
            "personal_email": "phoebe.buffay@friends.com",
            "employee": {}
        }
}
```

### /user_types/user_type.id/

* Description: delete one user type
* Method: DELETE
* Argument: user_type.id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: None
* Response body: 

```py
{
    "message": "User type deleted successfully"
}
```

## Service Routes

### /services/
* Description: get all services
* Method: GET
* Argument: None
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
[
    {
        "id": 1,
        "name": "Full Groom",
        "duration": 2.0,
        "price": 150.0
    },
    {
        "id": 2,
        "name": "Freshen Up",
        "duration": 1.0,
        "price": 80.0
    },
    {
        "id": 3,
        "name": "Tidy Up",
        "duration": 1.5,
        "price": 100.0
    },
    {
        "id": 4,
        "name": "Nails Only",
        "duration": 0.5,
        "price": 30.0
    }
]
```

### /services/service_id/
* Description: get one service by id
* Method: GET
* Argument: service_id
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
{
    "id": 1,
    "name": "Full Groom",
    "duration": 2.0,
    "price": 150.0
}
```

### /services/
* Description: create a new service
* Method: POST
* Argument: None
* Authentication: jwt bearer token
* Authorization: None
* Request body: 
  * required: name, duration, price

```py
{
    "name": "Cuddles and kissess",
    "duration": 0.5,
    "price": 30.00
}
```

* Request validations:
  * name must not already exist
  * price must be higher than 20.00 ($)
  * duration must be longer than 0.25 (hours)
* Response body: 

```py
{
    "id": 10,
    "name": "Cuddles And Kisses",
    "duration": 0.5,
    "price": 30.0,
    "bookings": []
}
```
  
### /services/service_id/

* Description: update one service's info
* Method: PUT, PATCH
* Argument: service_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: 
  * optional: name, duration, price

```py
{
    "duration": 0.5,
    "price": 50.00
}
```

* Request validations:
  * name must not already exist
  * price must be higher than 20.00 ($)
  * duration must be longer than 0.25 (hours)
* Response body: 

```py
{
    "id": 4,
    "name": "Cuddles And Kissess",
    "duration": 0.5,
    "price": 50.0,
    "bookings": []
}
```

### /services/service_id/

* Description: delete one service
* Method: DELETE
* Argument: service_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: None
* Response body: 

```py
{
    "message": "Service deleted successfully"
}
```

## Pet_type Routes

### /pet_types/
* Description: get all pet types
* Method: GET
* Argument: None
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
[
    {
        "id": 1,
        "name": "Dog"
    },
    {
        "id": 2,
        "name": "Cat"
    },
    {
        "id": 3,
        "name": "Bird"
    },
    {
        "id": 4,
        "name": "Mouse"
    },
    {
        "id": 5,
        "name": "Duck"
    }
]
```

### /pet_types/pet_type_id/
* Description: get one pet type
* Method: GET
* Argument: pet_type_id
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
{
    "id": 2,
    "name": "Cat"
}
```

### /pet_types/
* Description: create a pet type
* Method: POST
* Argument: None
* Authentication: jwt bearer token
* Authorization: admin ony
* Request body: 
  * required: name

```py
{
    "name": "crocodile"
}
```

* Request validations:
  * name must be longer than 2 characters and must not already exist

* Response body: 

```py
{
    "id": 6,
    "name": "Crocodile",
    "pets": []
}
```
  
### /pet_types/pet_type_id/

* Description: update one pet type
* Method: PUT, PATCH
* Argument: pet_type_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: 

```py
{
    "name": "horse"
}
```

* Request validations:
  * name must not already exist
  
* Response body: 

```py
{
    "id": 1,
    "name": "Horse",
    "pets": [
        {
            "id": 2,
            "name": "Mozzarella",
            "breed": "Cocker Spaniel",
            "year": 2019,
            "size": {
                "name": "M"
            },
            "type_id": 1,
            "size_id": 3,
            "client_id": 3
        },
        {
            "id": 3,
            "name": "Snoopy",
            "breed": "Beagle",
            "year": 2018,
            "size": {
                "name": "M"
            },
            "type_id": 1,
            "size_id": 3,
            "client_id": 6
        }
    ]
}
```

### /pet_types/pet_type_id/

* Description: delete one pet type
* Method: DELETE
* Argument: pet_type_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: None
* Response body: 

```py
{
    "message": "Pet type deleted successfully"
}
```


## Size Routes

### /sizes/
* Description: get all pet sizes
* Method: GET
* Argument: None
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
[
    {
        "id": 1,
        "weight": "<6kg",
        "name": "XS"
    },
    {
        "id": 2,
        "weight": "6-10kg",
        "name": "S"
    },
    {
        "id": 3,
        "weight": "10-25kg",
        "name": "M"
    },
    {
        "id": 4,
        "weight": ">25kg",
        "name": "L"
    }
]
```

### /sizes/size_id/
* Description: get one pet size by id
* Method: GET
* Argument: size_id
* Authentication: None
* Authorization: None
* Request body: None
* Response body: 

```py
{
    "id": 1,
    "weight": "<6kg",
    "name": "XS"
}
```

### /sizes/
* Description: create a new pet size
* Method: POST
* Argument: None
* Authentication: jwt bearer token
* Authorization: admin ony
* Request body: 
  * required: name, weight

```py
{
    "name": "Giant", 
    "weight": ">30 kg"
}
```

* Request validations:
  * name must not already exist

* Response body: 

```py
{
    "id": 5,
    "weight": ">30 kg",
    "name": "Giant",
    "pets": []
}
```
  
### /sizes/size_id/

* Description: update one pet size
* Method: PUT, PATCH
* Argument: size_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: 

```py
{
    "name": "Toy"
}
```

* Request validations:
  * name must not already exist
  
* Response body: 

```py
{
    "id": 1,
    "weight": "<6kg",
    "name": "Toy"
}
```

### /sizes/size_id/

* Description: delete one pet size
* Method: DELETE
* Argument: size_id
* Authentication: jwt bearer token
* Authorization: admin only
* Request body: None
* Response body: 

```py
{
    "message": "Pet size deleted successfully"
}
```

# The problem (Q1)  

Every business needs a reliable and efficient system to manage their clientele, workers and bookings. The purpose of this API application is to provide all-in-one management solution to a business that has the clients, staff and bookings as the core of their business model.  

With this application, users interact with the database using user-friendly RESTful API calls. Problems that can be solved by this application are:  
* Client management: adding, removing clients and reading or updating their information. 
* Staff management: adding, removing, reading and updating their information
* Roster planning: for the upcoming week by adding the required staff members into the work day
* Booking management: adding, removing, reading and updating bookings, with confirmation emails sent out to clients. 
* Data security: by authentication measures such as password log-in and authorization by multi-tired user privilege. 
* Data integrity: by valiation methods so that roster and bookings can be planned effectively.  

# Why do the problems need solving (Q2)  

Having a well-designed and user-friendly management system is essential to the operations of any business. It streamlines customer interactions, saves time and increases customer satisfaction.  

Similarly, proper staff and roster management ensure staff count is appropriate for expected work on a given day, and makes wage payment efficient.  

Data security provided with the application is important in protecting staff and clients' information from data breaches as well as ensuring the correctness of data in the database. 

# Database system (Q3)  
   
Database system chosen for the application is PostgreSQL due to the following advanatages:
* Open source (free)
* Compatible on all platforms (windows, Linux, MacOS)
* Widely used, supported and documented
* Strong reputation for reliability, scalability, extensibility and data integrity.
* Tools such as psycopg2 helps matching Python and PostgreSQL data types for seamless development process.

Drawbacks compared to other databases
* Memory performance
* Popularity
* https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems

### ORM (key functionalities and benefits) (Q4)
ORM stands for Object Relational Mapper, which supports the interactions between an application and its database.  

The chosen ORM for the project is SQLAlchemy becaude it is database-agnostic (which means it can be flexibily used with any databases), and it is highly compatible with Flask and Python.  

Key functionalities of ORM: 
- Instead of tables, entities are classes which extend the Model class 

```py
class Client(db.Model)
```

- Attributes are instances of Column class, data types are represented by CamelCase type or UPPERCASE types. 

```py
password = db.Column(db.String)
```

- Foreign keys are instances for ForeignKey class

```py
phone = db.Column(db.Integer, db.ForeignKey('users.phone'))
```

- Relationships between tables are represented by relationship method

```py
pets = db.relationship('Pet')
```

Key benefits of an ORM are:
- It allows the developers to query and manipulate database data using object-oriented programming language, therefore, it reduces the length and complexity of code compared to embedded SQL.
- It makes the development process easier because developers do not need to switch between OOP and SQL.  
- It has great support for tasks such as connections, seeds and migrations. As a result, implementation is straightforward. 
- It protects data from direct SQL injections because does not take explicit SQL queries and requires all interactions performed on OOP objects instead of  database tables.
- It is databse-agnostic which makes switching from one database (for development) to another one (for deployment) seamless whilst keeping the code base consistent. 

# Describe project models (Q8)
There are 10 models in the project, they are: User, Client, Employee, Pet, Booking, Sizes, Animal_type, User_type, Roster, and Service.  

1. Relationship between User model and Client model: one-and-only-one to zero-or-one relationship, where a user can be a client or not (an employee in this case) but a client can only be linked to one and only one user. User_id is a foreign key and primary key in the Client model because it is unique.
2. Relationship between User model and Employee model: one-and-only-one to zero-or-one relationship, where a user can be an employee or not (a client in this case) but an employee can only be linked to one and only one user. User_id is a foreign key and primary key in the Employee model because it is unique.
3. Relationship between User model and User_type model: one-and-only-one to zero-or-many relationship, where a user can only be of one and only one type (a client or an employee, but not both) and many users can be of one user_type or no users belongs to the user_type at all (all users are either clients or employees). Type_id is a foreign key in the User model, it is not nullable, and its values can have duplicates. 

4. Relationship between Employee model and Roster model: zero-or-many and one-and-only-one relationship, where an employee can have multiple rosters in their id, but they can also have none roster (in the case of new employee who has just signed up). A roster can only belong to one and only one employee. Employee_id is a foreign key in the Roster model, it is not nullable, and its values can have duplicates.
5. Relationship between Client model and Pet model: one-or-many and one-and-only-one relationship, where a client can have one or many pets, and a pet can belong to one and only one client. A client cannot be in the database without an associated pet, and vice versa. Client_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates. However, the combination of client_id and pet name has to be unique, for example Buddy is a common dog's name, therefore it can appear many times, a client whose id is 4, can only be associated one pet named Buddy.  
6. Relationship between Pet model and Size model: one-and-only-one to zero-or-many relationship, where a pet can only be of one and only one size, but a size can be shared amongst many pets, or none at all (in the case where no pet falls into the size category). Size_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates.
7. Relationship between Pet model and Animal_type model: one-and-only-one to zero-or-many relationship, where a pet can only be of one and only one type (dog or cat or duck), but a type can be shared amongst many pets, or none at all (in the case where no pet who is that type). Type_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates.
8. Relationship between Pet model and Booking model: one-and-only-one to one-or-many relationship, where a pet can have one or multiple bookings, and a booking can only associate with one and only one pet. A pet cannot be in the databse without a booking. Pet_id is a foreign key in the Booking model, it is not nullable, and its values can have duplicates. 
9.  Relationship between Booking model and Service model: one-and-only-one to zero-or-many relationship, where a booking is for one and only service, and a service can have multiple bookings or none at all associated with it. Service_id is a foreign key in the Booking model, it is not nullable, and its values can have duplicates. 
10. Relationship between Booking model and Employee model: one-and-only-one to zero-or-many relationship, where a booking can only be booked with one and only one employee, and an employee can be booked for many bookings or none at all (in the case of new employee who has just signed up). Employee_id is a foreign key in the booking model, it is not nullable, and its values can have duplicates.

# Describe project models (Q8)
There are 10 models in the project, they are: User, Client, Employee, Pet, Booking, Sizes, Animal_type, UserType, Roster, and Service.  
1. User model: 

Relationship with UserType model: one and only one to zero or many. The type_id is a foreign key, which links to the user_types.id in the UserType model. When a user_type is deleted, all associated users will be deleted.

Relationship with Client model: zero or one to one and only one. A user can be linked to one client or none (if the user is an employee) and a client can be linked to one and only one user. When a user is deleted, its associated client will also be removed.

Similarly, User model has zero or one to one and only one relationship. When a user is a client, they don't own an employee record, and one employee can only be linked to one and only one user. When a user is deleted, its associated employee will also be removed.

Model declaration:
```py
    type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'), nullable=False)
    
    type = db.relationship('UserType', back_populates = 'users')
    client = db.relationship('Client', back_populates = 'user', cascade = 'all, delete')
    employee = db.relationship('Employee', back_populates = 'user', cascade = 'all, delete')
```

Schema declaration:  
```py
    type = fields.Nested('UserTypeSchema', only = ['name'])
    employee = fields.Nested('EmployeeSchema', only = ['email', 'is_admin'])
```

In the UserSchema, TypeSchema and EmployeeSchema are nested, so that when the user is called, the returned is result is more meaningful, because it has type name, email address of the employee and tells if they are an admin not.

2. Client model: 

Relationship with User model: one and only one to zero or one relationship. When a client is deleted, its associated user record will also be removed.

Relationship with Pet model: zero or many to one and only one relationship. Ideally, a client can not exist in the database without a pet, but there are cases where a client owns more than one pet, and removing a pet should not remove the client from the database. As a result, cascade delete only goes one way in the relationship: if the client is deleted, their associated pets will be reomoved, but not vice versa.

Id is both a foreign key and primary key. It is linked to the id column in the User model, hence it is unique.

Model declaration:
```py
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    user = db.relationship('User', back_populates = 'client', cascade = 'all, delete')
    pets = db.relationship('Pet', back_populates = 'client', cascade = 'all, delete')
```

Schema declaration:
```py
    user = fields.Nested('UserSchema', exclude = ['employee', 'id'])
    pets = fields.List(fields.Nested('PetSchema', exclude = ['client']))
```

In the ClientSchema, UserSchema and PetSchema are nested. 'Employee' field is excluded to avoid circular imports,  and 'id' fields are excluded because it is the same as client's id. Similarly, 'client' field is excluded from PetSchema to avoid circular imports, and PetSchema is a list because a client can have many pets.

3. Employee model: 

Relationship with User model: one and only one to zero or one relationship. When an employee is deleted, its associated user record will also be removed.

Relationship with Booking model: zero or many to one and only one relationship. An employee can have many bookings, or none if they just started, and a booking can only belong to one and only one employee. When an employee is deleted, employee_id field in the Booking model will be set to null. 

Relationship with Roster model: zero or many to one and only one relationship. An employee can have many rosters, or none at all (if they just signed up and hasn't started), and a roster can belong to one and only one employee. When more than one employee is rostered on the same date, their rosters' id and employee_id are different, but the date are the same. When an employee is deleted, all associated rosters will also be removed, but removing a roster has no impact on the employee. 

Id is both a foreign key and primary key. It is linked to the id column in the User model, hence it is unique.

Model declaration:
```py
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)

    user = db.relationship('User', cascade = 'all, delete')
    bookings = db.relationship('Booking', back_populates = 'employee')
    rosters = db.relationship('Roster', back_populates = 'employee', cascade = 'all, delete')
```

Schema declaration:
```py
    user = fields.Nested('UserSchema', exclude = ['employee'])
    rosters = fields.List(fields.Nested('RosterSchema', exclude = ['employee']))
    bookings = fields.List(fields.Nested('BookingSchema', exclude = ['employee']))
```

In the EmployeeSchema, UserSchema, RosterSchema and BookingSchema are nested to provide more information about the employee. For example, the UserSchem has f_name, l_name, and phone and BookingSchema shows all bookings made with the employee. 'Employee' field has to be excluded in all cases to avoid circular imports. RosterSchema and BookingSchema are lists because an employee can have multiple bookings and rosters.

4. UserType model:

Relationship with User model: zero or many to one and only one relationship. A user_type can be used for zero or many users, but a user can only be of one and only one type. When a user_type is removed, type_id in the User model will be set to null, but when a user is deleted, it has no impacts on user_types. 

Model declaration:
```py
    users = db.relationship('User', back_populates = 'type', cascade = 'all, delete')
```

Schema declaration:
```py
    users = fields.List(fields.Nested('UserSchema', exclude=['type']))
```

In the UserTypeSchema, UserSchema is nested, so if a user_type is called, all users who are of that type will be shown. It is a list because there can be many users who fall into one type category.

5. Pet model:  

Relationship with Client model: zero or many to one and only one relationship. A client can have many or none pet (the pet passed away), but a pet can only belong to one and only one client. When a client is removed, all their associated pets will also be removed, but when a pet id removed, it has no impacts in the client. The client_id is a foreign key which links to the Client model. 

Relationship with Size model: one and only one to zero or many relationship. A pet can only be of one and only one size, but a size can be used by many pets or none at all. When a size is removed, corresponding pets will be removed, but when a pet is removed, it does not impact Size model. The size_id is a foereign key in the Pet model and links to the Size model. 

Relationship with Type model: one and only one to zero or many relationship. A pet can only be of one and only one type, but a type can be used by many pets or none at all. When a type is removed, corresponding pets will be removed, but when a pet is removed, it does not impact Type model. The type_id is a foereign key in the Pet model and links to the Type model. 

Relationship with Booking model: one or many to one and only one relationship. A pet must have at least one booking to be in the database, but they can only have many bookings. On the other hand, a booking can only belong to one and only one pet. When a pet is deleted, associated bookings will be removed, but removing a booking does not have any impacts on the pet.

The combination of pet's name, client_id and type_id has to be unique to avoid having duplications of the same pet in the database.

Model declaration:
```py
    type_id = db.Column(db.Integer, db.ForeignKey('pet_types.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    __table_args__ = (db.UniqueConstraint('name', 'client_id', 'type_id'),)

    client = db.relationship('Client', back_populates = 'pets')
    bookings = db.relationship('Booking', back_populates = 'pet', cascade = 'all, delete')
    type = db.relationship('PetType')
    size = db.relationship('Size')
```

Schema declaration:
```py
    client = fields.Nested('ClientSchema', only = ['user', 'id'])
    type = fields.Nested('PetTypeSchema', only = ['name'])
    size = fields.Nested('SizeSchema', only = ['name'])
    bookings = fields.List(fields.Nested('BookingSchema', exclude = ['pet']))
```

In the PetSchema, ClientSchema, PetTypeSchema, SizeSchema and BookingSchema are nested to provide all information regarding the pet. BookingSchema is a list because a pet can have many bookings. 'Pet' field is excluded from BookingSchema to avoid circular imports.

6. Size model:
Relationship with Pet model: zero or many to one and only one relationship. A size can be used for many pets or none at all, but a pet can only be of one and only one size. When a size is deleted, all pets of that size will also be removed (refuse service to one particular size of pets).

Model declaration:
```py
    pet = db.relationship('Pet', back_populates = 'size', cascade='all, delete')
``` 

Schema declaration:
```py
    pets = fields.List(fields.Nested('PetSchema', exclude = ['size']))
```

In the SizeSchema, PetSchema is nested so when a size is called, all pets who is of that size will also be shown. 'Size' field is excluded from PetSchema to avoid circular imports.

7. Type model:
Relationship with Pet model: zero or many to one and only one relationship. A type can be used for many pets or none at all, but a pet can only be of one and only one type. When a type is deleted, all pets of that type will also be removed (refuse service to one particular type of pets).

Model declaration:
```py
    pet = db.relationship('Pet', back_populates = 'size', cascade='all, delete')
``` 

Schema declaration:
```py
    pets = fields.List(fields.Nested('PetSchema', exclude = ['type']))
```

In the TypeSchema, PetSchema is nested so when a type is called, all pets who is of that type will also be shown. 'Type' field is excluded from PetSchema to avoid circular imports.

8. Booking Model
Relationship with Pet model: one and only one to one or many. A pet can have one or many bookings (has to have at least one), and a booking can only be booked for one and only one pet. When a pet is deleted, all associated bookings will also be removed, but when a booking is deleted, it has no effect on the pet (one way cascade delete). Pet_id is a foreign key that links the Booking model to the id colummn in Pet model.

Relationship with Employee model: one and only one to zero or many. An employee can have zero or many bookings, and a booking can only be booked for one and only one employee. When an employee is deleted, employee_id in the Booking model is set to null. When a booking is deleted, it has no effect on the employee (one way cascade delete). Employee_id is a foreign key that links the Booking model to the id column in Employee model.

Relationship with Service model: one and only one to zero or many. A booking can be booked for one and only one service, and a service can be used in zero (new service just got added) or many bookings. When a service is deleted, related bookings will also be removed, but when a booking is deleted, it has no effect on the service. Service_id is a foreign key that links the Booking model to the id column in Service model.

The combination of pet_id, date and time is unique to avoid double booking. 

Model declaration:

```py
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='SET NULL'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('pet_id', 'date', 'time'),)

    pet = db.relationship('Pet', back_populates = 'bookings')
    employee = db.relationship('Employee')
    service = db.relationship('Service', back_populates = 'bookings')
```

Schema declaration: 

```py
    pet = fields.Nested('PetSchema', exclude = ['bookings'])
    service = fields.Nested('ServiceSchema', exclude = ['id', 'bookings'])
    employee = fields.Nested('EmployeeSchema', only = ['user'])
```

In the BookingSchema, PetSchema, ServiceSchema and EmployeeSchema are nested, so when a booking is called, all information on the pet, the groomer and the service are also presented. 'Bookings' field are excluded from PetSchema and ServiceSchema to avoid circular imports.

9. Service Model
Relationship with Booking model: one and only to zero or many. A service can be used in zero or many bookings, and a booking can only be made for one and only one service. When a service is deleted, related bookings are also removed.

Model declaration:

```py
    bookings = db.relationship('Booking', back_populates = 'service', cascade = 'all, delete')
```

Schema declaration:

```py
    bookings = fields.List(fields.Nested('BookingSchema', exclude=['service']))
```

In the ServiceSchema, BookingSchema is nested and it is a list because there are many bookings associated with a service type. 

10. Roster model:
Relationship with Employee model: zero or many to one and only one. An employee can be assigned to many rosters (or none if they just signed up), and a roster can only be assigned to one and only one employee. If more than one employees are rostered on the same date, their rosters will have different ids and diffrent employee_ids but the same date. When an employee is deleted, all their rosters will be removed, but removing the rosters has no effect on the employee.  

Employee_id is a foreign key in the Roster model, it links to the id column in the Employee model.

A combination of employee_id and date are unique to avoid double rostering an employee. 

Model declaration:

```py
  employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

  employee = db.relationship('Employee', back_populates = 'rosters')
```

Schema declaration:

```py
  employee = fields.Nested('EmployeeSchema', only = ['user'])
```

In the RosterSchema, EmployeeSchema is nested so if a roster is called, employee information is also presented. 

# Discuss the database relations (Q9)
There are 10 relations/tables in the database.  

1. Users table - includes all the users, they are divided into 2 types: employees and clients. 
* Attributes in the users table are: id (serial, not null, primary key), f_name (string, not null), l_name (string, not null), phone (string, not null and unique), personal_email (string, optional), and date created (date data type, automatically set to current date). 
* When a user is deleted, the associated fields in the clients and employees table are also deleted (cascade delete)
* Foreign key is type_id (int, not null), which links to the user_types table. On delete, related records are to be removed.
* Relationships: 
  * users - clients: zero or one to one and only one relationship
  * users - employees: zero or one to one and only one relationship
  * users - user_types: one and only one to zero or many relationship

2. Clients table - includes all the users who are clients. 
* Attributes of the clients table are: id (which is also user_id, serial, primary key), password (string, optional). If a client wants to make bookings online, or edit their profile, track their bookings, they need to sign up. If a client does not sign up, password field will be null. Passwords are stored as hashed in the database.
* When a client is removed, their associated info in the users table will also be removed (cascade delete).Similarly, any pets they own, will also be removed (cascade delete).
* Relationships: 
  * clients - users: one and only one to one and only one relationship
  * clients - pets: zero or many to one and only one relationship

3. Employees table - includes all the users who are employees. 
* Attributes of the employees table are: id (which is also user_id, serial, primary key), email (string, not null), password (string, not null), is_admin (boolean, not null, default is 'False'). Passwords are stored as hashed.
* When an employee is removed, their associated info in the users table will also be removed (cascade delete)
* Relationships: 
  * employees - users:
  * employees - rosters:
  * employees - bookings:

4. User_types table - information on user types. There are 2 types: client and employee 
* Attributes of the user_types table are: id (serial, primary key), name (string, not null). 
* When a user type is deleted, all related records in users table will be removed (cascade delete).
* Relationship: user_types - users: zero or many to one and only one relationship. 

5. Pets table - includes all clients' pets. It is important to know the type and size of the animal because they influence the time required to groom it. The age of the pet is also worth knowing as some older animals are prone to having heart attacks. 
* Attributes of the pets table are: id (serial, primary key), name (string, not null), breed (string, optional, default: unknown), year (int, not null) 
* Foreign keys: client_id (int, not null), size_id (int, not null), type_id (int, not null)
* When a client is deleted, associated pets will be removed (cascade delete), but when the pet is removed, the client can stay in the database as they may own other pets.
* Relationships: 
  * pets - clients: zero or many to one and only one relationship. A pet can belong to one and only one client, but a client can have many pets, or zero if the pet passed away.
  * pets - sizes: one and only one to zero or many relationship. A pet can only be of one and only one size, and a size can be set for many pets or zero if no pets fall into the size range.
  * pets - types: one and only one to zero or many relationship. A pet can only be of one and only one type (cat or dog or duck), and a type can be set for many pets or zero if no pets fall into the type category.
  * pets - bookings: one or many to one and only one relationship. A pet can have one or many bookings, but it cannot be in the system without any bookings. A booking can only belong to one and only one pet. 

6. Sizes table: information on animal's weights and corresponding sizes. This information is important because it influences the time needed to groom the animal. 
* Attributes are: id (serial, primary key), weight (int, not null), size (string, nut null). 
* Relationship:
  * sizes - pets: zero or many to one and only one relationship. A pet can be of only one size, but a size can be used for many pets, or none at all. 

7. Animal_types table: information on the types of pets
* Attributes are: id (serial, primary key), name (string, not null)
* Relationship: 
  * animal_types - pets: zero or many to one and only one relationship. A type can be used in for many pets or none at all (new type that just got added), but a pet can be of one and only one type. 

8. Bookings table - includes all bookings. 
* Attributes are: id (serial, primary key), date (date, not null), time (time, not null), status (string, not null). Booking date and time have to be in the future. Valid statuses are: pending, in progress and completed. 
* Foreign keys are: pet_id (int, not null), employee_id (int, default is null), service_id (int, not null). A client can choose to book with a specific employee, if not specified, whoever is rostered on the day will do the job. 
* When a pet is deleleted, all associated bookings will also be removed (cascade delete). When an employee is deleted, the employee_id field in associated bookings will be set to null. 
* Relationships: 
  * bookings - pets: one or many to one and only one relationship. A booking can only associate with one and only one pet, a pet can have one or many bookings. 
  * bookings - employees: one and only one to zero or many relationship. A booking can only associate with one and only one employee, but an employee can have many bookings or none at all (if they just started). 
  * bookings - services: one and only one to zero or many relationship. A booking can only be booked for one and only one service, but a service can be used in many bookings, or none at all. 

9. Services table - information on the services available at the salon
* Attributes are: id (serial, primary key), name (string, not null), duration (float, not null), price (float, not null). 
* Relationship: 
  * services - bookings: zero or many to one and only one relationship. A service can be booked for many bookings or none at all (example: a new service), and a booking can only be booked for one and only one service. 

10. Rosters table - all roster information
* Attributes are: id (serial, primary key), date (date, not null), employee_id (int, not null). The combination of date and employee_id is set to unique to avoid double booking an employee for the same date. 
* Relationship:
  * rosters - employees: zero or many to one and only one relationship. An employee can have many rosters or none at all, and each roster can only belong to one and only one employee. Example: if they are 2 employees rostered for the work day of 2022-12-01, the rosters are [roster id #1, date: 2022-12-01, employee_id: 1] and [roster id #2, date: 2022-12-01, employee_id: 2].


# Planning and tracking of tasks (Q10)

The project is divided into three main parts:
* Initial planning
* Writing code
* Writing documentation 

Initial planning includes:
1. Brainstorming ideas for an application that is meaningful and suitable to my skill level. 
2. Get approval for the idea
3. What features to be included in the app
4. What entities that need tracking to achieve the said features
5. What are the relationships between said entities
6. What are the API endpoints
7. What are the CRUD operations that are appropriate for each entity
8. What is the Database Management System to be used


After the initial planning, each task is executed through 3 stages writing code, testing and documentation.  

Task #1: Create the skeletal structure of the application
* Code: create a virtual environment, install all the required dependencies, initialize the application, a PostgreSQL database, and a git repository.
* Testing: test the index route (landing page)
* Documentation: complete R1, R2, R3 of the documentation requirements 

Task #2: 'Create the clients entity, Client model'
* Code: create the client model and ClientSchema, cli command to create and seed the table in the database. 
* Testing: test the psql database to check if a seeded table is created
* Documentation: first part of R4

Task #3: Create API endpoints for CRUD operations on clients entity
* Code: create the client blueprint, register it and API endpoints for CRUD operations. Create errorhandlers
* Testing: test all the CRUD operations on clients entity
* Documentation: first part of R5

Task #4 and Task #5: same process of Task #2 and Task #3, but on 'pets' entity

Task #6 and Task #7: same process of Task #2 and Task #3, but on 'staff' entity

Task #8 and Task #9: same process of Task #2 and Task #3, but on 'bookings' entity

Task #10 and Task #11: same process of Task #2 and Task #3, but on 'rosters' entity
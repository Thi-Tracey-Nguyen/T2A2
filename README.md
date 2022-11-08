### The problem (Q1)  

Every business needs a reliable and efficient system to manage their clientele, workers and bookings. The purpose of this API application is to provide all-in-one management solution to a business that has the clients, staff and bookings as the core of their business model.  

With this application, users interact with the database using user-friendly RESTful API calls. Problems that can be solved by this application are:  
* Client management: adding, removing clients and reading or updating their information. 
* Staff management: adding, removing, reading and updating their information
* Roster planning: for the upcoming week by adding the required staff members into the work day
* Booking management: adding, removing, reading and updating bookings, with confirmation emails sent out to clients. 
* Data security: by authentication measures such as password log-in and authorization by multi-tired user privilege. 
* Data integrity: by valiation methods so that roster and bookings can be planned effectively.  

### Why do the problems need solving (Q2)  

Having a well-designed and user-friendly management system is essential to the operations of any business. It streamlines customer interactions, saves time and increases customer satisfaction.  

Similarly, proper staff and roster management ensure staff count is appropriate for expected work on a given day, and makes wage payment efficient.  

Data security provided with the application is important in protecting staff and clients' information from data breaches as well as ensuring the correctness of data in the database. 

### Database system (Q3)  
   
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

### Describe project models (Q8)
There are 10 models in the project, they are: User, Client, Employee, Pet, Booking, Sizes, Animal_type, User_type, Roster, and Service.  

1. Relationship between User model and Client model: one-and-only-one to zero-or-one relationship, where a user can be a client or not (an employee in this case) but a client can only be linked to one and only one user. User_id is a foreign key and primary key in the Client model because it is unique.
2. Relationship between User model and Employee model: one-and-only-one to zero-or-one relationship, where a user can be an employee or not (a client in this case) but an employee can only be linked to one and only one user. User_id is a foreign key and primary key in the Employee model because it is unique.
3. Relationship between User model and User_type model: one-and-only-one to zero-or-many relationship, where a user can only be of one and only one type (a client or an employee, but not both) and many users can be of one user_type or no users belongs to the user_type at all (all users are either clients or employees). Type_id is a foreign key in the User model, it is not nullable, and its values can have duplicates. 
4. Relationship between Employee model and Roster model: zero-or-many and one-and-only-one relationship, where an employee can have multiple rosters in their id, but they can also have none roster (in the case of new employee who has just signed up). A roster can only belong to one and only one employee. Employee_id is a foreign key in the Roster model, it is not nullable, and its values can have duplicates.
5. Relationship between Client model and Pet model: one-or-many and one-and-only-one relationship, where a client can have one or many pets, and a pet can belong to one and only one client. A client cannot be in the database without an associated pet, and vice versa. Client_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates. However, the combination of client_id and pet name has to be unique, for example Buddy is a common dog's name, therefore it can appear many times, a client whose id is 4, can only be associated one pet named Buddy.  
6. Relationship between Pet model and Size model: one-and-only-one to zero-or-many relationship, where a pet can only be of one and only one size, but a size can be shared amongst many pets, or none at all (in the case where no pet falls into the size category). Size_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates.
7. Relationship between Pet model and Animal_type model: one-and-only-one to zero-or-many relationship, where a pet can only be of one and only one type (dog or cat or duck), but a type can be shared amongst many pets, or none at all (in the case where no pet who is that type). Type_id is a foreign key in the Pet model, it is not nullable, and its values can have duplicates.
8. Relationship between Pet model and Booking model: one-and-only-one to one-or-many relationship, where a pet can have one or multiple bookings, and a booking can only associate with one and only one pet. A pet cannot be in the databse without a booking. Pet_id is a foreign key in the Booking model, it is not nullable, and its values can have duplicates. 
9. Relationship between Booking model and Service model: one-and-only-one to zero-or-many relationship, where a booking is for one and only service, and a service can have multiple bookings or none at all associated with it. Service_id is a foreign key in the Booking model, it is not nullable, and its values can have duplicates. 
10. Relationship between Booking model and Employee model: one-and-only-one to zero-or-many relationship, where a booking can only be booked with one and only one employee, and an employee can be booked for many bookings or none at all (in the case of new employee who has just signed up). Employee_id is a foreign key in the booking model, it is not nullable, and its values can have duplicates.

### Discuss the database relations (Q9)
There are 10 relations/tables in the database.
1. 

11. Planning and tracking of tasks

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
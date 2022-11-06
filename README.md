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

Key benefits of an ORM are:
- It allows the developers to query and manipulate database data using object-oriented programming language, therefore, it reduces the length and complexity of code compared to embedded SQL.
- It makes the development process easier because developers do not need to switch between OOP and SQL.  
- It has great support for tasks such as connections, seeds and migrations. As a result, implementation is straightforward. 
- It protects data from direct SQL injections because does not take explicit SQL queries and requires all interactions performed on OOP objects instead of  database tables.
- It is databse-agnostic which makes switching from one database (for development) to another one (for deployment) seamless whilst keeping the code base consistent. 

1.  Planning and tracking of tasks

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
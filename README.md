1. The problem  

Every business needs a reliable and efficient system to manage their clientele, workers and bookings. The purpose of this API application is to provide all-in-one management solution to a business that has the clients, staff and bookings as the core of their business model.  

With this application, users interact with the database using user-friendly RESTful API calls. Problems that can be solved by this application are:  
* Client management: adding, removing clients and reading or updating their information. 
* Staff management: adding, removing, reading and updating their information
* Roster planning: for the upcoming week by adding the required staff members into the work day
* Booking management: adding, removing, reading and updating bookings, with confirmation emails sent out to clients. 
* Data security: by authentication measures such as password log-in and authorization by multi-tired user privilege. 
* Data integrity: by valiation methods so that roster and bookings can be planned effectively.  

2. Why do the problems need solving  

Having a well-designed and user-friendly management system is essential to the operations of any business. It streamlines customer interactions, saves time and increases customer satisfaction.  

Similarly, proper staff and roster management ensure staff count is appropriate for expected work on a given day, and makes with wage payment fast and precise.  

Data security provided with the application is important in protecting staff and clients' information from data breaches as well as ensuring the correctness of data in the database. 

3. Database system  
   
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



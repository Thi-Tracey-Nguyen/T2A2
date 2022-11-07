from datetime import date
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.client import Client
from models.employee import Employee
from models.pet_type import PetType
from models.pet import Pet
from models.size import Size
from models.user_type import UserType
from models.user import User
from models.service import Service
from models.booking import Booking
from models.roster import Roster


db_commands = Blueprint('db', __name__)

#function to generate client or employee object based on user info
def generate_record():
    stmt = db.select(User)
    records = db.session.scalars(stmt)
    for record in records:
        if record.type_id == 1:
            new_record = Client(id = record.id)
        else:
            email = record.f_name.lower() + '.' + record.l_name.lower() + '@dogspa.com'
            password = record.f_name[:2] + record.f_name[-2:] + record.l_name[0] + record.l_name[-1] + 'ds123'
            new_record = Employee(
                id = record.id, 
                email = email, 
                password = bcrypt.generate_password_hash(password).decode('utf8')
            )
        db.session.add(new_record)
        db.session.commit()

        
@db_commands.cli.command('create')
def create_table():
    db.create_all()
    print('Tables created!')


@db_commands.cli.command('drop')
def drop_table():
    db.drop_all()
    print('Tables dropped!')

@db_commands.cli.command('seed')
def seed_table():
    user_types = [
    UserType(
        name = 'Client'
    ),
    UserType(
        name = 'Employee'
    )
    ]

    db.session.add_all(user_types)
    db.session.commit()


    users = [
    User(
        f_name = 'Rachel',
        l_name = 'Green',
        phone = '300573',
        date_created = date.today(),
        type_id = 1
        
    ),
    User(
        f_name = 'Phoebe',
        l_name = 'Buffay',
        phone = '779149',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Joey',
        l_name = 'Tribbiani',
        phone = '271746',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Chandler',
        l_name = 'Bing',
        phone = '871413',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Ross',
        l_name = 'Geller',
        phone = '702162',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Gunther',
        l_name = 'Adkins',
        phone = '927623',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Carol',
        l_name = 'Frye',
        phone = '449866',
        date_created = date.today(),
        type_id = 1,
    ),
    User(
        f_name = 'Estelle',
        l_name = 'Leonard',
        phone = '184288',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Richard',
        l_name = 'Burke',
        phone = '129049',
        date_created = date.today(),
        type_id = 1
    ),
    User(
        f_name = 'Dwight',
        l_name = 'Schrute',
        phone = '975150',
        date_created = date.today(),
        type_id = 2
    ),
    User(
        f_name = 'Michael',
        l_name = 'Scott',
        phone = '657403',
        date_created = date.today(),
        type_id = 2
    ),
    User(
        f_name = 'Jim',
        l_name = 'Halpert',
        phone = '349082',
        date_created = date.today(),
        type_id = 2
    ),
    User(
        f_name = 'Cathy',
        l_name = 'Simms',
        phone = '754022',
        date_created = date.today(),
        type_id = 2
    ),
    ]

    db.session.add_all(users)
    db.session.commit()

    generate_record()

    admin_user = User(
        f_name = 'admin',
        l_name = 'admin',
        phone = '000000',
        type_id = 2
    )
    
    db.session.add(admin_user)
    db.session.commit()

    #generate admin employee
    admin_stmt = db.select(User).filter_by(phone = '000000')
    admin = db.session.scalar(admin_stmt)
    admin_employee = Employee(
        id = admin.id,
        email = 'admin@dogspa.com',
        password = bcrypt.generate_password_hash('admin123!').decode('utf8'),
        is_admin = True
    )

    db.session.add(admin_employee)
    db.session.commit()

    pet_types = [
    PetType(
        name = 'Dog'
    ),
    PetType(
        name = 'Cat'
    ),
    PetType(
        name = 'Bird'
    ),
    PetType(
        name = 'Mouse'
    ),
    PetType(
        name = 'Duck'
    )
    ]

    sizes = [
    Size(
        weight = '<6kg',
        name = 'XS'
    ),
    Size(
        weight = '6-10kg',
        name = 'S'
    ),
    Size(
        weight = '10-25kg',
        name = 'M'
    ),
    Size(
        weight = '>25kg',
        name = 'L'
    ),
    ]

    db.session.add_all(pet_types)
    db.session.add_all(sizes)
    db.session.commit()

    pets = [
    Pet(
        name = 'Donald',
        type_id = 5,
        client_id = 4,
        size_id = 1,
        year = 2022
    ),
    Pet(
        name = 'Mozzarella',
        type_id = 1,
        breed = 'Cocker Spaniel',
        size_id = 3,
        client_id = 3,
        year = 2019
    ),
    Pet(
        name = 'Snoopy',
        type_id = 1,
        breed = 'Beagle',
        size_id = 3,
        client_id = 6,
        year = 2018
    ),
    Pet(
        name = 'Grumpy',
        type_id = 2,
        breed = 'Short-haired',
        size_id = 2,
        client_id = 4,
        year = 2020
    ),
    Pet(
        name = 'Garfield',
        type_id = 2,
        breed = 'Short-haired',
        size_id = 2,
        client_id = 5,
        year = 2020
    )
    ]

    services = [
    Service(
        name = 'Full Groom',
        duration = 2,
        price = 150.00
    ),
    Service(
        name = 'Freshen Up',
        duration = 1,
        price = 80.00
    ),
    Service(
        name = 'Tidy Up',
        duration = 1.5,
        price = 100.00
    ),
    Service(
        name = 'Nails Only',
        duration = 0.5,
        price = 30.00
    )]

    db.session.add_all(pets)
    db.session.add_all(services)
    db.session.commit()

    bookings = [
    Booking(
        pet_id = 1,
        employee_id = 10,
        service_id = 1,
        date = '2022-12-11',
        time = '10:00'
    ),
    Booking(
        pet_id = 2,
        service_id = 2,
        employee_id = 12,
        date = '2022-12-18',
        time = '13:00'
    ),
    Booking(
        pet_id = 3,
        service_id = 3,
        employee_id = 11,
        date = '2022-12-21',
        time = '09:00'
    ),
    Booking(
        pet_id = 4,
        service_id = 1,
        employee_id = 13,
        date = '2022-12-21',
        time = '09:00'
    )
    ]

    rosters = [
    Roster(
        date = '2022-12-01',
        employee_id = 10
    ),
    Roster(
        date = '2022-12-01',
        employee_id = 11
    ),
    Roster(
        date = '2022-12-01',
        employee_id = 12
    ),
    Roster(
        date = '2022-12-02',
        employee_id = 10
    ),
    Roster(
        date = '2022-12-02',
        employee_id = 11
    ),
    Roster(
        date = '2022-12-02',
        employee_id = 12
    ),
    Roster(
        date = '2022-12-03',
        employee_id = 10
    ),
    Roster(
        date = '2022-12-03',
        employee_id = 11
    ),
    Roster(
        date = '2022-12-03',
        employee_id = 13
    ),
    Roster(
        date = '2022-12-04',
        employee_id = 12
    ),
    Roster(
        date = '2022-12-04',
        employee_id = 13
    ),
    Roster(
        date = '2022-12-04',
        employee_id = 11
    ),
    Roster(
        date = '2022-12-05',
        employee_id = 12
    ),
    Roster(
        date = '2022-12-05',
        employee_id = 13
    ),
    Roster(
        date = '2022-12-05',
        employee_id = 10
    ),
    Roster(
        date = '2022-12-06',
        employee_id = 10
    ),
    Roster(
        date = '2022-12-06',
        employee_id = 11
    ),
    Roster(
        date = '2022-12-06',
        employee_id = 13
    ),
    Roster(
        date = '2022-12-07',
        employee_id = 12
    ),
    Roster(
        date = '2022-12-07',
        employee_id = 13
    ),
    Roster(
        date = '2022-12-07',
        employee_id = 11
    ),
    ]

    db.session.add_all(bookings)
    db.session.add_all(rosters)
    db.session.commit()
    print('Table seeded!')

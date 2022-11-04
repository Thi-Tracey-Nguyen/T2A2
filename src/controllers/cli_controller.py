from datetime import date
from flask import Blueprint
from init import db
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


db_commands = Blueprint('db', __name__)

def generate_record():
    stmt = db.select(User)
    records = db.session.scalars(stmt)
    for record in records:
        if record.type_id == 1:
            new_record = Client(user_id = record.id)
        else:
            email = record.f_name + '.' + record.l_name + '@dog_spa.com'
            new_record = Employee(user_id = record.id, email = email)
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
    User(
        f_name = 'Pam',
        l_name = 'Beesly',
        phone = '279531',
        date_created = date.today(),
        type_id = 2
    ),
    User(
        f_name = 'Angela',
        l_name = 'Martin',
        phone = '558709',
        date_created = date.today(),
        type_id = 2
    ),
    ]

    db.session.add_all(users)
    db.session.commit()

    generate_record()

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
        employee_id = 1,
        service_id = 1,
        date = '2022-12-11',
        time = '10:00'
    ),
    Booking(
        pet_id = 2,
        service_id = 2,
        employee_id = 2,
        date = '2022-12-18',
        time = '13:00'
    ),
    Booking(
        pet_id = 3,
        service_id = 3,
        employee_id = 3,
        date = '2022-12-21',
        time = '09:00'
    ),
    Booking(
        pet_id = 4,
        service_id = 1,
        employee_id = 4,
        date = '2022-12-21',
        time = '09:00'
    )
    ]

    db.session.add_all(bookings)
    db.session.commit()
    print('Table seeded!')

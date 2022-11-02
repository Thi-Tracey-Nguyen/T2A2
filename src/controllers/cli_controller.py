from flask import Blueprint
from init import db
from models.user import User
from models.client import Client
from models.staff import Staff
from models.pet_type import PetType
from models.pet import Pet
from models.size import Size
from models.user_type import UserType
from models.user import User


db_commands = Blueprint('db', __name__)

def generate_record():
    stmt = db.select(User)
    records = db.session.scalars(stmt)
    for record in records:
        if record.type_id == 1:
            new_record = Client(user_id = record.id)
        else:
            email = record.f_name + '.' + record.l_name + '@dog_spa.com'
            new_record = Staff(user_id = record.id, email = email)
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
        name = 'Staff'
    )
    ]

    db.session.add_all(user_types)
    db.session.commit()


    users = [
    User(
        f_name = 'Rachel',
        l_name = 'Green',
        phone = '300573',
        type_id = 1
    ),
    User(
        f_name = 'Phoebe',
        l_name = 'Buffay',
        phone = '779149',
        type_id = 1
    ),
    User(
        f_name = 'Joey',
        l_name = 'Tribbiani',
        phone = '271746',
        type_id = 1
    ),
    User(
        f_name = 'Chandler',
        l_name = 'Bing',
        phone = '871413',
        type_id = 1
    ),
    User(
        f_name = 'Ross',
        l_name = 'Geller',
        phone = '702162',
        type_id = 1
    ),
    User(
        f_name = 'Gunther',
        l_name = 'Adkins',
        phone = '927623',
        type_id = 1
    ),
    User(
        f_name = 'Carol',
        l_name = 'Frye',
        phone = '449866',
        type_id = 1,
    ),
    User(
        f_name = 'Estelle',
        l_name = 'Leonard',
        phone = '184288',
        type_id = 1
    ),
    User(
        f_name = 'Richard',
        l_name = 'Burke',
        phone = '129049',
        type_id = 1
    ),
    User(
        f_name = 'Dwight',
        l_name = 'Schrute',
        phone = '975150',
        type_id = 2
    ),
    User(
        f_name = 'Michael',
        l_name = 'Scott',
        phone = '657403',
        type_id = 2
    ),
    User(
        f_name = 'Jim',
        l_name = 'Halpert',
        phone = '349082',
        type_id = 2
    ),
    User(
        f_name = 'Cathy',
        l_name = 'Simms',
        phone = '754022',
        type_id = 2
    ),
    User(
        f_name = 'Pam',
        l_name = 'Beesly',
        phone = '279531',
        type_id = 2
    ),
    User(
        f_name = 'Angela',
        l_name = 'Martin',
        phone = '558709',
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
        name = 'Duck',
        type_id = 5,
        client_id = 4,
        size_id = 1,
        year = 2022
    ),
    Pet(
        name = 'Mozzarella',
        type_id = 1,
        size_id = 3,
        client_id = 3,
        year = 2019
    )
    ]
    db.session.add_all(pets)
    db.session.commit()
    print('Table seeded!')

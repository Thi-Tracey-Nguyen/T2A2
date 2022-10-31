from flask import Blueprint
from init import db
from models.client import Client


db_commands = Blueprint('db', __name__)

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
    clients = [
    Client(
        f_name = 'Rachel',
        l_name = 'Green',
        phone = '300573',
        email = 'rachel.green@friends.com',
    ),
    Client(
        f_name = 'Phoebe',
        l_name = 'Buffay',
        phone = '779149',
        email = 'phoebe.buffay@friends.com',
    ),
    Client(
        f_name = 'Joey',
        l_name = 'Tribbiani',
        phone = '271746',
        email = 'joey.tribbiani@foo.com',
    ),
    Client(
        f_name = 'Chandler',
        l_name = 'Bing',
        phone = '871413',
        email = 'chandler.bing@friends.com',
    ),
    Client(
        f_name = 'Ross',
        l_name = 'Geller',
        phone = '702162',
        email = 'ross.geller@spam.com',
    ),
    Client(
        f_name = 'Gunther',
        l_name = 'Adkins',
        phone = '927623',
        email = 'gunther.adkins@spam.com',
    ),
    Client(
        f_name = 'Carol',
        l_name = 'Frye',
        phone = '449866',
        email = 'carol.frye@friends.com',
    ),
    Client(
        f_name = 'Estelle',
        l_name = 'Leonard',
        phone = '184288',
        email = 'estelle.leonard@foo.com',
    ),
    Client(
        f_name = 'Richard',
        l_name = 'Burke',
        phone = '129049',
        email = 'richard.burke@friends.com',
    )
    ]
    db.session.add_all(clients)
    db.session.commit()
    print('Table seeded!')

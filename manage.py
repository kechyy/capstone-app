from flask_script import Manager
from sqlalchemy import Column, String, Integer, create_engine
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Movie, Actor

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# custom seed command
@manager.command
def seed():
    Movie(title='Sugar Rush', release_date='2019-12-12').insert()
    Movie(title='Mary Men', release_date='2016-08-12').insert()
    Movie(title='The next Level', release_date='2003-12-12').insert()
    Movie(title='Frozen 2', release_date='2009-11-12').insert()

    Actor(name='Marlon Brando', age=60, gender='male').insert()
    Actor(name='Leonardo DiCaprio', age=50, gender='male').insert()
    Actor(name='AI Pacino', age=29, gender='male').insert()
    Actor(name='Jack Nicholson', age=30, gender='male').insert()

if __name__ == '__main__':
    manager.run()
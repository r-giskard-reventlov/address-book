from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI
from seldon_address_book import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

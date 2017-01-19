import os
parent_dir = os.path.abspath(os.path.dirname(os.pardir))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(parent_dir, 'db/rabpubs.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
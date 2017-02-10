import os
app_root = os.path.abspath(__file__ + "/../../")

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_root, 'db/rabpubs.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_BASE = 'https://dvivocit1.services.brown.edu/rabpubs/'
REST_BASE = 'https://dvivocit1.services.brown.edu/rabdata/'

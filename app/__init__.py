from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from config import ConfigMain

app = Flask(__name__)
app.app_context().push()
app.config.from_object(ConfigMain)
app.config['SQLALCHEMY_DATABASE_URI'] = ConfigMain.SQLALCHEMY_DATABASE_URI_0
UPLOADED_FILES_DEST_ITEM = ConfigMain.UPLOADED_FILES_DEST_ITEM
UPLOADED_FILES_DEST_USER = ConfigMain.UPLOADED_FILES_DEST_USER

ma = Marshmallow(app)
db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager(app)


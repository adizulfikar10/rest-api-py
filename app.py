from flask import Flask
from flask_seeder import FlaskSeeder
from api import category_bp, transaction_bp
from api.models.db import db
from flask_migrate import Migrate
from api.models import Base
from api.db import engine
import os
from dotenv import load_dotenv
from flask_seeder import FlaskSeeder
from flask_cors import CORS


app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for frontend
CORS(app, origins=["http://localhost:3000"])

app.register_blueprint(category_bp, url_prefix='/api')
app.register_blueprint(transaction_bp, url_prefix='/api')

# Flask-Migrate setup
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Seeder setup
seeder = FlaskSeeder()
seeder.init_app(app, db)

if __name__ == '__main__':
    app.run(debug=True,port=5050)
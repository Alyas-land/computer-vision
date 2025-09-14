from flask import Flask
from extensions import db
import os

app = Flask(__name__, template_folder='views')

project_path = os.getcwd()
database_path = os.path.join(project_path + '\\database')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}/computer_vision.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db.init_app(app)
import model.models

@app.before_request
def createDatabase():
    db.create_all()
    print("Tables created.")

from controller.home import Main
app.add_url_rule("/", view_func=Main.as_view("main"))

from api.route import SendData, VideoFeed
# URL routes
app.add_url_rule("/status", view_func=SendData.as_view("send_data"), methods=['GET'])
app.add_url_rule("/video_feed", view_func=VideoFeed.as_view("video_feed"))

if (__name__ == '__main__'):
    # with app.app_context():  # Needed for DB operations
    #     db.create_all()
    app.run()
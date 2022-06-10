from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        try:
            return check_password_hash(self.password, password)
        except AttributeError:
            return False


class Images(db.Model):
    __table_args__ = (
        db.UniqueConstraint("img_id"),
    )
    id = db.Column(db.Integer, primary_key=True)
    img_id = db.Column(db.String(12), nullable=False)
    img_url = db.Column(db.String(150), nullable=False)
    img_address = db.Column(db.String(150), nullable=False)
    img_width = db.Column(db.Integer, nullable=True)
    img_height = db.Column(db.Integer, nullable=True)


class Favorites(db.Model):
    fav_id = db.Column(db.Integer, primary_key=True)
    fav_img_id = db.Column(db.String(12), nullable=False)
    fav_img_url = db.Column(db.String(150), nullable=False)
    fav_img_address = db.Column(db.String(150), nullable=False)
    fav_img_width = db.Column(db.Integer, nullable=True)
    fav_img_height = db.Column(db.Integer, nullable=True)
    user_mail = db.Column(db.String(150), nullable=False)


db.create_all()
# for each in range(1, 5):
#     url = "https://wallhaven.cc/api/v1/search"
#     key = "TyGuzQ0QcwIluIoD1mUhi2bCEyIpNUtu"
#     payload = {"apikey": key, "sorting": "favorites", "purity": "100", "page": each}
#     r = requests.get(url, params=payload)
#     res = r.json()
#     wallpapers_numb = res["data"]
#     db.create_all()
#
#     for i in range(1, len(wallpapers_numb)):
#         img_id = res["data"][i]["id"]
#         img_url = res["data"][i]["path"]
#         img_address = res["data"][i]["url"]
#         img_width = res["data"][i]["dimension_x"]
#         img_height= res["data"][i]["dimension_y"]
#
#         image = Images(img_id=img_id, img_url=img_url, img_address=img_address, img_width=img_width, img_height=img_height)
#         db.session.add(image)
#         db.session.commit()

# images = Images.query.all()
# for each in images:
#     print(each.img_url)

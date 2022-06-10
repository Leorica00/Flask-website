from config import Images, Favorites, Users
from flask import Flask, request, render_template, flash, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'shalvalomtadze00@outlook.com'
app.config['MAIL_PASSWORD'] = 'paroli123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)




@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "" or password == "":
            flash("შეიყვანეთ ყველა მონაცემი")
        elif email != "" or password != "":
            all_emails = Users.query.filter_by(email=email).first()

            if all_emails == [] or all_emails is None or all_emails.check_password(password) is False:
                flash("მომხმარებლის იმეალი ან პაროლი არასოწრია")
            else:
                # try:
                    msg = Message("Flask Login",
                                      sender="shalvalomtadze00@outlook.com",
                                      recipients=[email],
                                      body="You have successfully logged in.")
                    mail.send(msg)
                    session['username'] = email
                    return redirect(url_for("user"))
                # except:
                #     flash("მომხმარებელი ამ იმეილით არ მოიძებნა")
    else:
        return render_template("login.html")
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if email == "" or username == "" or password == "":
            flash("შეიყვანეთ ყველა მონაცემი")
        else:
            user = Users(username=username, email=email, password=password)
            user.set_password(password)
            all_usernames = Users.query.filter_by(username=username).all()
            all_emails = Users.query.filter_by(email=email).all()

            if all_usernames == [] and all_emails == []:
                db.session.add(user)
                db.session.commit()
                try:
                    msg = Message("Flask registration",
                                  sender="shalvalomtadze00@outlook.com",
                                  recipients=[email],
                                  body="Congratulations, you have successfully registered on our website")
                    mail.send(msg)
                    return render_template("login.html")
                except:
                    flash("მომხმარებელი ამ იმეილით არ მოიძებნა")
            else:
                flash("მომხარებელი ამ სახელით ან იმეილით უკვე არსებობს")
    return render_template('register.html')


@app.route('/user')
def user():
    if 'username' in session:
        images = Images.query.all()
        return render_template("user.html", images=images)
    else:
        return render_template('login.html')


@app.route('/user/<id>', methods=["POST", "GET"])
def user_id(id):
    images = Images.query.filter_by(img_id=id).first()
    if request.method == "POST":
        if request.form["add_to_fav"] == "Add to favorites":
            images = Images.query.filter_by(img_id=id).first()
            if images != []:
                userMail = session["username"]
                fav_img = Favorites(fav_img_id=images.img_id, fav_img_url=images.img_url,
                                    fav_img_address=images.img_address, fav_img_width=images.img_width,
                                    fav_img_height=images.img_height, user_mail=userMail)
                db.create_all()
                db.session.add(fav_img)
                db.session.commit()
            return render_template("img.html", image_id=id, images=images)

    return render_template("img.html", image_id=id, images=images)


@app.route('/add_image', methods=['POST', 'GET'])
def add_image():
    if request.method == "POST":
        try:
            id = request.form["id"]
            img_url = request.form["img_url"]
            url = request.form["img_address"]
            img_width = request.form["img_width"]
            img_height = request.form["img_height"]
            if id == "" or img_url == "" or url == "":
                flash("შეიყვანეთ ყველა საჭირო მონაცემი")
            else:
                img = Images(img_id=id, img_url=img_url, img_address=url, img_width=img_width, img_height=img_height)
                db.session.add(img)
                db.session.commit()
                return render_template("user.html")
        except:
            flash("სურათის id არ არის უნიკალური")
    return render_template("add_img.html")


@app.route('/favorites')
def favorites():
    userMail = session["username"]
    favorites = Favorites.query.filter_by(user_mail=userMail).all()
    return render_template("favorites.html", favorites=favorites)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)

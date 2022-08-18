import random
import string
from datetime import datetime

# import pymysql
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash
)
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from exts import mail, db
from models import EmailCaptchaModel, UserModel
from blueprints.forms import RegisterForm, LoginForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email2 = form.email.data
            password2 = form.password.data
            user = UserModel.query.filter_by(email=email2).first()
            # db.commit()
            if user and check_password_hash(user.password, password2):
                session['user_id'] = user.id
                return redirect("/user")
            else:
                flash("Email或密碼輸入錯誤")
                return redirect(url_for("user.login"))
        else:
            flash("Email或密碼格式錯誤")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email1 = form.email.data
            username1 = form.username.data
            password1 = form.password.data

            # md5("zhiliao") = sdafsdfasfsdfsda
            hash_password = generate_password_hash(password1)
            user = UserModel(email=email1, username=username1, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('user.login'))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    # GET,POST
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="註冊認證碼",
            recipients=[email],
            body=f"您申請的驗證碼是：{captcha}"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha:", captcha)
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "請先填入Email！"})


@bp.route("/joblist", methods=['GET', 'POST'])
def joblist():
    datalist = []
    con = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='practiceproject',
        charset='utf8'
    )
    cur = con.cursor()
    job = request.form.get("q")
    print(job)
    if job is None:
        datalist = []
        sql = 'select jobtitle,joburl,company,city,salary,source from job where salary like "%月%";'
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            datalist.append(item)
        cur.close()
        # print(datalist)
        return render_template("joblist.html", joblist=datalist)
    elif job is not None:
        sql = f"select jobtitle,joburl,company,city,salary,source from job where jobcat like '%{{job}}%' and salary like '%月%'"
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            datalist.append(item)
        cur.close()
        # print(datalist)
        return render_template("joblist.html", joblist=datalist)


@bp.route("/", methods=['GET'])
def about():
    return render_template("toppage.html")


@bp.route("/dashboard", methods=['GET'])
def dashboard():
    return render_template("dashboard.html")

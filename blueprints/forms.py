import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=4, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    @staticmethod
    def validate_email(field):
        email1 = field.data
        user_model = UserModel.query.filter_by(email=email1).first()
        if user_model:
            raise wtforms.ValidationError("Email重複註冊！")

    def validate_captcha(self, field):
        captcha = field.data
        email1 = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email1).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("驗證碼錯誤！")


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])


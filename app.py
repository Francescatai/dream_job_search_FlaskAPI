from flask import Flask, session, g, render_template
from flask_migrate import Migrate

import config
from blueprints import qa_bp
from blueprints import user_bp
from exts import db, mail
from models import UserModel

app = Flask(__name__)
app.config['SERVER NAME'] = 'jobsearch.com:5000'
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

''' 確認用戶 '''
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
        except:
            g.user = None


@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}

''' 首頁 '''
@app.route("/", methods=['GET'], redirect_to='/user')
def about():
    return render_template("toppage.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")

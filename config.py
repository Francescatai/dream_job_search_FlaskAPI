
''' 數據庫配置 '''
HOSTNAME = 'localhost'
PORT     = '3306'
DATABASE = 'practiceproject'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True


SECRET_KEY = "kljfigjopemvfiirgjr"


'''  EMAIL配置 '''
MAIL_SERVER = ""
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = ""

import os
from flask import Flask, redirect, url_for
from models import db
from shop_routes import shop_bp
from admin_routes import admin_bp

app = Flask(__name__)

# تحديد المسار المطلق للمشروع وقاعدة البيانات المحلية
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tshoot-secret-key-2026')

# الاعتماد على متغير البيئة DATABASE_URL في Render إذا وجد، وإلا استخدام SQLite محلياً
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # إصلاح دعم روابط postgres:// القديمة لتتوافق مع SQLAlchemy
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات
db.init_app(app)

# تسجيل الـ Blueprints
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)

# إنشاء الجداول عند التشغيل
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('shop.login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
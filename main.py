import os
from flask import Flask
from models import db
from shop_routes import shop_bp

app = Flask(__name__)

# إعدادات قاعدة البيانات وسرية الجلسات
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tshoot-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات مع التطبيق
db.init_app(app)

# تسجيل الـ Blueprint الخاص بالمحل
app.register_blueprint(shop_bp)

# إنشاء الجداول عند تشغيل التطبيق لأول مرة
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('shop.login'))

if __name__ == '__main__':
    # قراءة المنفذ المخصص من الاستضافة السحابية أو استخدام 5000 محلياً
    port = int(os.environ.get('PORT', 5000))
    # التشغيل على 0.0.0.0 ليكون متاحاً على الشبكة والسحاب
    app.run(host='0.0.0.0', port=port)
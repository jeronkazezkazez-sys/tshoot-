code = """from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import db, Shop, RepairTicket

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        shop = Shop.query.filter_by(phone=phone, password=password).first()
        if shop:
            session['shop_id'] = shop.id
            return redirect(url_for('shop.dashboard'))
        flash('رقم الهاتف أو كلمة المرور غير صحيحة', 'danger')
    return render_template('shop_login.html')

@shop_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        shop_name = request.form.get('shop_name')
        owner_name = request.form.get('owner_name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        existing_shop = Shop.query.filter_by(phone=phone).first()
        if existing_shop:
            flash('رقم الهاتف مستخدم مسبقاً', 'danger')
            return redirect(url_for('shop.register'))
            
        new_shop = Shop.create_shop(shop_name, owner_name, phone, password)
        session['shop_id'] = new_shop.id
        flash('تم تسجيل المحل بنجاح!', 'success')
        return redirect(url_for('shop.dashboard'))
    return render_template('shop_register.html')

@shop_bp.route('/dashboard')
def dashboard():
    if 'shop_id' not in session:
        return redirect(url_for('shop.login'))
    
    shop = Shop.query.get(session['shop_id'])
    tickets = RepairTicket.query.filter_by(shop_id=shop.id).all()
    
    return render_template('shop_dashboard.html', shop=shop, tickets=tickets)

@shop_bp.route('/add-ticket', methods=['POST'])
def add_ticket():
    if 'shop_id' not in session:
        return redirect(url_for('shop.login'))
    
    customer_name = request.form.get('customer_name')
    device_name = request.form.get('device_name')
    status = request.form.get('status', 'قيد الصيانة')
    
    new_ticket = RepairTicket(
        customer_name=customer_name,
        device_name=device_name,
        status=status,
        shop_id=session['shop_id']
    )
    db.session.add(new_ticket)
    db.session.commit()
    flash('تم إضافة تذكرة الصيانة بنجاح', 'success')
    return redirect(url_for('shop.dashboard'))

@shop_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('shop.login'))
"""

with open("shop_routes.py", "w", encoding="utf-8") as f:
    f.write(code)

print("تم إنشاء ملف shop_routes.py بالصيغة الصحيحة بنجاح!")
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import db, Shop, RepairTicket

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        shop = Shop.query.filter_by(phone=phone).first()
        if shop and shop.check_password(password):
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
            
        Shop.create_shop(shop_name, owner_name, phone, password)
        new_shop = Shop.query.filter_by(phone=phone).first()
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
    customer_phone = request.form.get('customer_phone', 'غير متوفر')
    device_model = request.form.get('device_model')
    issue_description = request.form.get('issue_description', 'صيانة عامة')
    status = request.form.get('status', 'قيد الفحص')
    cost = float(request.form.get('cost', 0.0) or 0.0)
    
    new_ticket = RepairTicket(
        customer_name=customer_name,
        customer_phone=customer_phone,
        device_model=device_model,
        issue_description=issue_description,
        status=status,
        cost=cost,
        shop_id=session['shop_id']
    )
    db.session.add(new_ticket)
    db.session.commit()
    flash('تم إضافة تذكرة الصيانة بنجاح', 'success')
    return redirect(url_for('shop.dashboard'))

@shop_bp.route('/ticket/<int:ticket_id>/print')
def print_ticket(ticket_id):
    if 'shop_id' not in session:
        return redirect(url_for('shop.login'))
    
    shop = Shop.query.get(session['shop_id'])
    ticket = RepairTicket.query.filter_by(id=ticket_id, shop_id=shop.id).first_or_404()
    
    return render_template('print_ticket.html', shop=shop, ticket=ticket)

@shop_bp.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
def delete_ticket(ticket_id):
    if 'shop_id' not in session:
        return redirect(url_for('shop.login'))
    
    shop = Shop.query.get(session['shop_id'])
    ticket = RepairTicket.query.filter_by(id=ticket_id, shop_id=shop.id).first_or_404()
    
    db.session.delete(ticket)
    db.session.commit()
    flash('تم حذف تذكرة الصيانة بنجاح', 'success')
    return redirect(url_for('shop.dashboard'))

@shop_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('shop.login'))
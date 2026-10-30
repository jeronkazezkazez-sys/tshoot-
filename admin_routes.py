from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import db, Shop, RepairTicket
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'tshoot2026':
            session['is_admin'] = True
            return redirect(url_for('admin.dashboard'))
        flash('بيانات الدخول غير صحيحة', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin.admin_login'))
    
    shops_activity = db.session.query(
        Shop,
        db.func.count(RepairTicket.id).label('total_tickets')
    ).outerjoin(RepairTicket).group_by(Shop.id).order_by(db.func.count(RepairTicket.id).desc()).all()

    return render_template('admin_dashboard.html', shops_activity=shops_activity)

@admin_bp.route('/update-subscription/<int:shop_id>', methods=['POST'])
def update_subscription(shop_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin.admin_login'))
        
    shop = Shop.query.get_or_404(shop_id)
    months_to_add = int(request.form.get('months', 1))
    
    shop.is_paid = True
    base_date = shop.subscription_end_date if (shop.subscription_end_date and shop.subscription_end_date > datetime.utcnow()) else datetime.utcnow()
    
    shop.subscription_end_date = base_date + timedelta(days=(months_to_add * 30))
    
    db.session.commit()
    flash(f'تم تفعيل اشتراك محل {shop.shop_name} بنجاح لمدة {months_to_add} أشهر.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.admin_login'))
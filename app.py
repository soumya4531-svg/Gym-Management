import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from models import db, Admin, Member, Subscription, Payment
from datetime import datetime, date
import calendar

# Load environment variables
load_dotenv()

import urllib.parse
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

# Use SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'gym.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Helper function to check if user is logged in
def is_logged_in():
    return 'admin_id' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    members = Member.query.all()
    subscriptions = Subscription.query.all()
    return render_template('dashboard.html', members=members, subscriptions=subscriptions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if not is_logged_in():
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email') or None
        phone = request.form.get('phone')
        subscription_id = request.form.get('subscription_id')
        weight = request.form.get('weight')
        height = request.form.get('height')
        medical_condition = request.form.get('medical_condition') or None
        
        fitness_goal = request.form.get('fitness_goal') or None
        workout_monday = request.form.get('workout_monday') or None
        workout_tuesday = request.form.get('workout_tuesday') or None
        workout_wednesday = request.form.get('workout_wednesday') or None
        workout_thursday = request.form.get('workout_thursday') or None
        workout_friday = request.form.get('workout_friday') or None
        workout_saturday = request.form.get('workout_saturday') or None
        workout_sunday = request.form.get('workout_sunday') or None
        
        # Validation
        if not all([first_name, last_name, phone]):
            flash('Please fill out all required fields.', 'error')
            return redirect(url_for('add_member'))
            
        sub_id = int(subscription_id) if subscription_id else None
        # Handle photo upload
        photo_filename = None
        photo = request.files.get('photo')
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            photo_filename = unique_filename
        
        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            subscription_id=sub_id,
            photo_filename=photo_filename,
            weight=float(weight) if weight else None,
            height=float(height) if height else None,
            medical_condition=medical_condition,
            fitness_goal=fitness_goal,
            workout_monday=workout_monday,
            workout_tuesday=workout_tuesday,
            workout_wednesday=workout_wednesday,
            workout_thursday=workout_thursday,
            workout_friday=workout_friday,
            workout_saturday=workout_saturday,
            workout_sunday=workout_sunday,
            subscription_start=datetime.utcnow().date() if sub_id else None
        )
        
        try:
            db.session.add(new_member)
            db.session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding member. Email might already exist.', 'error')
            
    subscriptions = Subscription.query.all()
    return render_template('add_member.html', subscriptions=subscriptions)

@app.route('/add_subscription', methods=['GET', 'POST'])
def add_subscription():
    if not is_logged_in():
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        duration = request.form.get('duration_months')
        price = request.form.get('price')
        
        if not all([name, duration, price]):
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('add_subscription'))
            
        try:
            new_sub = Subscription(
                name=name,
                duration_months=int(duration),
                price=float(price)
            )
            db.session.add(new_sub)
            db.session.commit()
            flash('Subscription plan added successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid duration or price format.', 'error')
            
    return render_template('add_subscription.html')

@app.route('/delete_member/<int:id>', methods=['POST'])
def delete_member(id):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member removed successfully!', 'success')
    return redirect(url_for('index'))

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

@app.route('/member/<int:id>')
def member_insight(id):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    member = Member.query.get_or_404(id)
    
    # Calculate payment status
    status = "No Subscription"
    expiration_date = None
    if member.subscription and member.subscription_start:
        expiration_date = add_months(member.subscription_start, member.subscription.duration_months)
        if date.today() <= expiration_date:
            status = "Active"
        else:
            status = "Expired"
            
    return render_template('member_insight.html', member=member, status=status, expiration_date=expiration_date)

@app.route('/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    member = Member.query.get_or_404(id)
    
    if request.method == 'POST':
        member.first_name = request.form.get('first_name')
        member.last_name = request.form.get('last_name')
        member.email = request.form.get('email') or None
        member.phone = request.form.get('phone')
        
        weight = request.form.get('weight')
        height = request.form.get('height')
        member.weight = float(weight) if weight else None
        member.height = float(height) if height else None
        member.medical_condition = request.form.get('medical_condition') or None
        
        subscription_id = request.form.get('subscription_id')
        new_sub_id = int(subscription_id) if subscription_id else None
        
        # If subscription changed, update start date
        if new_sub_id != member.subscription_id:
            member.subscription_id = new_sub_id
            member.subscription_start = datetime.utcnow().date() if new_sub_id else None
        
        # Handle photo upload
        photo = request.files.get('photo')
        if photo and photo.filename:
            # Delete old photo if exists
            if member.photo_filename:
                old_path = os.path.join(app.config['UPLOAD_FOLDER'], member.photo_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = secure_filename(photo.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            member.photo_filename = unique_filename
        
        # Handle photo removal
        if request.form.get('remove_photo') == '1' and member.photo_filename:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], member.photo_filename)
            if os.path.exists(old_path):
                os.remove(old_path)
            member.photo_filename = None
        
        if not all([member.first_name, member.last_name, member.phone]):
            flash('First name, last name, and phone are required.', 'error')
            subscriptions = Subscription.query.all()
            return render_template('edit_member.html', member=member, subscriptions=subscriptions)
        
        try:
            db.session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('member_insight', id=member.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating member.', 'error')
    
    subscriptions = Subscription.query.all()
    return render_template('edit_member.html', member=member, subscriptions=subscriptions)

@app.route('/member/<int:id>/edit_workout', methods=['GET', 'POST'])
def edit_workout(id):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    member = Member.query.get_or_404(id)
    
    if request.method == 'POST':
        member.fitness_goal = request.form.get('fitness_goal') or None
        member.workout_monday = request.form.get('workout_monday') or None
        member.workout_tuesday = request.form.get('workout_tuesday') or None
        member.workout_wednesday = request.form.get('workout_wednesday') or None
        member.workout_thursday = request.form.get('workout_thursday') or None
        member.workout_friday = request.form.get('workout_friday') or None
        member.workout_saturday = request.form.get('workout_saturday') or None
        member.workout_sunday = request.form.get('workout_sunday') or None
        
        try:
            db.session.commit()
            flash('Fitness goal and workout routine updated successfully!', 'success')
            return redirect(url_for('member_insight', id=member.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating workout routine.', 'error')
            
    return render_template('edit_workout.html', member=member)

@app.route('/member/<int:id>/subscription_overview')
def subscription_overview(id):
    if not is_logged_in():
        return redirect(url_for('login'))
        
    member = Member.query.get_or_404(id)
    
    if not member.subscription or not member.subscription_start:
        flash('This member has no subscription.', 'info')
        return redirect(url_for('member_insight', id=id))
    
    sub_start = member.subscription_start
    total_sub_months = member.subscription.duration_months
    monthly_fee = round(member.subscription.price / total_sub_months, 2)
    today = date.today()
    
    # Dynamic range: show from subscription start month
    # to at least 12 months, or current month + 3, whichever is further
    months_since_start = (today.year - sub_start.year) * 12 + (today.month - sub_start.month)
    total_to_show = max(12, total_sub_months, months_since_start + 4)
    
    months = []
    for i in range(total_to_show):
        m = sub_start.month + i
        y = sub_start.year
        while m > 12:
            m -= 12
            y += 1
        
        if i < total_sub_months:
            # Within subscription period — paid via subscription
            status = 'paid'
            source = 'Subscription'
            # Payment date for subscription months = subscription start date
            paid_date = sub_start
        else:
            # Beyond subscription — check manual payments
            payment = Payment.query.filter_by(member_id=id, month=m, year=y).first()
            if payment and payment.is_paid:
                status = 'paid'
                source = 'Manual Payment'
                paid_date = payment.paid_date.date() if payment.paid_date else None
            else:
                status = 'due'
                source = None
                paid_date = None
        
        months.append({
            'index': i,
            'month': m,
            'year': y,
            'label': date(y, m, 1).strftime('%B %Y'),
            'amount': monthly_fee,
            'status': status,
            'source': source,
            'paid_date': paid_date,
        })
    
    return render_template('subscription_overview.html', member=member, months=months, monthly_fee=monthly_fee, today=today)

@app.route('/mark_paid/<int:member_id>/<int:month>/<int:year>', methods=['POST'])
def mark_paid(member_id, month, year):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    member = Member.query.get_or_404(member_id)
    monthly_fee = round(member.subscription.price / member.subscription.duration_months, 2) if member.subscription else 0
    
    # Accept custom payment date from the form
    paid_date_str = request.form.get('paid_date')
    if paid_date_str:
        try:
            paid_dt = datetime.strptime(paid_date_str, '%Y-%m-%d')
        except ValueError:
            paid_dt = datetime.utcnow()
    else:
        paid_dt = datetime.utcnow()
    
    payment = Payment.query.filter_by(member_id=member_id, month=month, year=year).first()
    if not payment:
        payment = Payment(
            member_id=member_id,
            month=month,
            year=year,
            amount=monthly_fee,
            is_paid=True,
            paid_date=paid_dt
        )
        db.session.add(payment)
    else:
        payment.is_paid = True
        payment.paid_date = paid_dt
    
    db.session.commit()
    flash(f'Payment marked as paid for {date(year, month, 1).strftime("%B %Y")}!', 'success')
    return redirect(url_for('subscription_overview', id=member_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default admin if none exists
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin / admin123")
            
    app.run(debug=True)

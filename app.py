from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash  # ДОБАВЛЕН generate_password_hash
from datetime import datetime
from models import db, User, Ship, Permit, CatchLog, Inspection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = ""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- НОВИЙ МАРШРУТ ЗА РЕГИСТРАЦИЯ ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Хешируем пароль для безопасности
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        # Создаем нового пользователя
        new_user = User(username=request.form['username'], password=hashed_password)

        # Проверяем, нет ли уже такого пользователя
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user:
            flash('Това потребителско име вече е заето!', 'danger')
            return redirect(url_for('register'))

        db.session.add(new_user)
        db.session.commit()
        flash('Успешна регистрация! Сега можете да влезете.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# -------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Невалидни данни!', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    ships = Ship.query.all()
    return render_template('index.html', ships=ships)


@app.route('/permits')
@login_required
def permits():
    all_permits = Permit.query.all()
    return render_template('permits.html', permits=all_permits)


@app.route('/permit/add', methods=['GET', 'POST'])
@login_required
def add_permit():
    if request.method == 'POST':
        new_permit = Permit(
            permit_number=request.form['permit_number'],
            issue_date=datetime.strptime(request.form['issue_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date(),
            gear_type=request.form['gear_type'],
            ship_id=request.form['ship_id']
        )
        db.session.add(new_permit)
        db.session.commit()
        flash('Разрешителното е издадено успешно!', 'success')
        return redirect(url_for('permits'))
    ships = Ship.query.all()
    return render_template('add_permit.html', ships=ships)


@app.route('/permit/revoke/<int:permit_id>')
@login_required
def revoke_permit(permit_id):
    permit = Permit.query.get_or_404(permit_id)
    permit.is_active = False
    db.session.commit()
    flash(f'Разрешителното {permit.permit_number} е отнето успешно!', 'warning')
    return redirect(url_for('permits'))


@app.route('/catch_logs')
@login_required
def catch_logs():
    logs = CatchLog.query.order_by(CatchLog.date.desc()).all()
    return render_template('catch_logs.html', logs=logs)


@app.route('/catch_log/add', methods=['GET', 'POST'])
@login_required
def add_catch_log():
    if request.method == 'POST':
        new_log = CatchLog(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            fish_species=request.form['fish_species'],
            quantity_kg=float(request.form['quantity_kg']),
            ship_id=request.form['ship_id']
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Уловът е записан успешно!', 'success')
        return redirect(url_for('catch_logs'))
    ships = Ship.query.all()
    return render_template('add_catch_log.html', ships=ships)


@app.route('/catch_log/delete/<int:log_id>')
@login_required
def delete_catch_log(log_id):
    log = CatchLog.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash('Записът за улова е изтрит!', 'info')
    return redirect(url_for('catch_logs'))


@app.route('/inspections')
@login_required
def inspections():
    all_inspections = Inspection.query.order_by(Inspection.date.desc()).all()
    return render_template('inspections.html', inspections=all_inspections)


@app.route('/inspection/add', methods=['GET', 'POST'])
@login_required
def add_inspection():
    if request.method == 'POST':
        new_insp = Inspection(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            location=request.form['location'],
            result=request.form['result'],
            violations=request.form['violations'],
            ship_id=request.form['ship_id']
        )
        db.session.add(new_insp)
        db.session.commit()
        flash('Инспекцията е записана успешно!', 'success')
        return redirect(url_for('inspections'))
    ships = Ship.query.all()
    return render_template('add_inspection.html', ships=ships)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
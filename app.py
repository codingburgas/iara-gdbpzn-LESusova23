from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Ship, User, Permit  # Добавили Permit
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # Добавили для работы с датами

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vash-super-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        ships = Ship.query.all()
        return render_template('index.html', ships=ships)
    else:
        return render_template('landing.html')


@app.route('/ship/add', methods=['GET', 'POST'])
@login_required
def add_ship():
    if request.method == 'POST':
        # Создаем объект судна со всеми полями
        new_ship = Ship(
            name=request.form['name'],
            int_number=request.form['int_number'],
            call_sign=request.form.get('call_sign', ''),
            marking=request.form.get('marking', ''),
            owner_name=request.form['owner_name'],
            captain_name=request.form['captain_name'],
            # Преобразуем числовые поля, если они пустые - ставим 0.0
            length=float(request.form['length']) if request.form['length'] else 0.0,
            width=float(request.form['width']) if request.form['width'] else 0.0,
            tonnage=float(request.form['tonnage']) if request.form['tonnage'] else 0.0,
            draft=float(request.form['draft']) if request.form['draft'] else 0.0,
            engine_power=float(request.form['engine_power']) if request.form['engine_power'] else 0.0,
            fuel_type=request.form.get('fuel_type', '')
        )

        db.session.add(new_ship)
        db.session.commit()
        flash('Корабът е добавен успешно в регистъра!', 'success')
        return redirect(url_for('index'))

    return render_template('add_ship.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Потребител с това име вече съществува! Моля, изберете друго.', 'danger')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрацията е успешна! Моля, влезте.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неправилно потребителско име или парола!', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/permits')
@login_required
def permits():
    # Получаем все разрешения из базы
    all_permits = Permit.query.all()
    return render_template('permits.html', permits=all_permits)


@app.route('/permit/add', methods=['GET', 'POST'])
@login_required
def add_permit():
    if request.method == 'POST':
        # Преобразуем строки из HTML-формы в объекты Python Date
        i_date = datetime.strptime(request.form['issue_date'], '%Y-%m-%d').date()
        e_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()

        new_permit = Permit(
            permit_number=request.form['permit_number'],
            issue_date=i_date,
            expiry_date=e_date,
            gear_type=request.form['gear_type'],
            ship_id=request.form['ship_id']  # ID корабля из выпадающего списка
        )
        db.session.add(new_permit)
        db.session.commit()
        flash('Разрешителното е издадено успешно!', 'success')
        return redirect(url_for('permits'))

    # Для GET-запроса (отрисовка формы) нам нужен список всех кораблей для выбора
    ships = Ship.query.all()
    return render_template('add_permit.html', ships=ships)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Ship, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vash-super-secret-key-123' # Не забудьте сменить на свой секретный ключ!
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
        new_ship = Ship(
            name=request.form['name'],
            int_number=request.form['int_number'],
            owner_name=request.form['owner_name'],
            captain_name=request.form['captain_name']
        )
        db.session.add(new_ship)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_ship.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=request.form['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрацията е успешна! Моля, влезте.', 'success')
        return redirect(url_for('index')) # Возврат на главную (лендинг)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index')) # Успешный вход — сразу в систему
        else:
            flash('Неправилно потребителско име или парола!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) # Выход — обратно на лендинг

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
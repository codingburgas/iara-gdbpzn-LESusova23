from flask import Flask, render_template, request, redirect, url_for
from models import db, Ship

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():

    ships = Ship.query.all()
    return render_template('index.html', ships=ships)


@app.route('/ship/add', methods=['GET', 'POST'])
def add_ship():
    if request.method == 'POST':
        # Получаем данные из формы
        new_ship = Ship(
            name=request.form['name'],
            int_number=request.form['int_number'],
            owner_name=request.form['owner_name'],
            captain_name=request.form['captain_name']
        )
        # Сохраняем в базу данных
        db.session.add(new_ship)
        db.session.commit()
        # Возвращаемся на главную
        return redirect(url_for('index'))

    # Если это просто переход по ссылке (GET) - показываем форму
    return render_template('add_ship.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
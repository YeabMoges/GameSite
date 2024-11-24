from flask import Flask, render_template, request, redirect, url_for, session, flash
from search_results import search_games
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import bcrypt, pymysql, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning

db = SQLAlchemy(app)
load_dotenv()


# Setting up RDS connection
def connect_to_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # For hashed passwords
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)


@app.route('/')
def home():
    # You no longer need to fetch any Steam or Google Play data.
    return render_template('home.html')


# Fetch results from RDS table
def fetch_games(table_name):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            games = cursor.fetchall()  # Get all rows as a list of dictionaries
    finally:
        connection.close()
    return games


def fetch_mobile_games():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM mobile_games")  # Query all rows from mobilegame table
            games = cursor.fetchall()  # Fetch all results as a list of dictionaries
    finally:
        connection.close()
    return games


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            return redirect(url_for('my_account'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        phone_number = request.form['phone_number']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create and save the new user
        user = User(username=username, password=hashed_password.decode('utf-8'),
                    email=email, address=address, phone_number=phone_number)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            flash('Error: Username or email already exists.', 'danger')

    return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.email = request.form['email']
        user.address = request.form['address']
        user.phone_number = request.form['phone_number']
        db.session.commit()
        flash('Account updated successfully!', 'success')

    return render_template('my_account.html', user=user)


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()  # Get the search query
    results = search_games(query)  # Call the function from search_results.py
    return render_template('search_results.html', query=query, results=results)


@app.route('/shop')
def shop():
    # Placeholder logic for shop
    return "Welcome to the Shop! (This page is under construction.)"


@app.route('/cart')
def cart():
    # Placeholder logic for the cart
    return "Your shopping cart is currently empty!"


@app.route('/action-games')
def action_games():
    games = fetch_games('action_games')  # Fetch games from the database
    genre_videos = [  # Action-specific videos
        'liQLtCLq3tc',
        'AKXiKBnzpBQ',
        '5fIAPcVdZO8'
    ]
    return render_template('genre_games.html', genre='Action', games=games, genre_videos=genre_videos)


@app.route('/adventure-games')
def adventure_games():
    games = fetch_games('adventure_games')
    genre_videos = [
        'A88YiZdXugA',
        'f28nKLp-eKg',
        'D9w97KSEAOo'
    ]
    return render_template('genre_games.html', genre='Adventure', games=games, genre_videos=genre_videos)


# Route for Early Access Games
@app.route('/earlyaccess-games')
def earlyaccess_games():
    games = fetch_games('earlyaccess_games')
    genre_videos = [
        '-f_--CwFsNo',
        'iU9ZiJQBTqE',
        '4ms-LHkN6YQ'
    ]
    return render_template('genre_games.html', genre='Early Access', games=games, genre_videos=genre_videos)


# Route for Free Games
@app.route('/free-games')
def free_games():
    games = fetch_games('free_games')
    genre_videos = [
        'Odj7pIsHRt0',
        'PyMlV5_HRWk',
        'c80dVYcL69E'
    ]
    return render_template('genre_games.html', genre='Free to Play', games=games, genre_videos=genre_videos)


# Add additional routes for each genre as needed
@app.route('/indie-games')
def indie_games():
    games = fetch_games('indie_games')
    genre_videos = [
        'SgSX3gOrj60',
        'bVbyn7c1X6E',
        'FcITAzKW3fY'
    ]
    return render_template('genre_games.html', genre='Indie', games=games, genre_videos=genre_videos)


@app.route('/mmo-games')
def mmo_games():
    games = fetch_games('mmo_games')
    genre_videos = [
        'dZrxWFrd1zQ',
        'W8WFJN2syoM',
        'kp4WrQp6pUg'
    ]
    return render_template('genre_games.html', genre='MMO', games=games, genre_videos=genre_videos)


@app.route('/rpg-games')
def rpg_games():
    games = fetch_games('rpg_games')
    genre_videos = [
        'BtyBjOW8sGY',
        '6umhTJQltak',
        'FOMhUJitBD4'
    ]
    return render_template('genre_games.html', genre='RPG', games=games, genre_videos=genre_videos)


@app.route('/simulation-games')
def simulation_games():
    games = fetch_games('simulation_games')
    genre_videos = [
        '5uvwfskYwl0',
        'pzgPXOw2plI',
        '7vlKoMi4Qr0'
    ]
    return render_template('genre_games.html', genre='Simulation', games=games, genre_videos=genre_videos)


@app.route('/sports-games')
def sports_games():
    games = fetch_games('sports_games')
    genre_videos = [
        'CYncAnd31Q8',
        '9ewiJJe_nYI',
        'XhP3Xh4LMA8'
    ]
    return render_template('genre_games.html', genre='Sports', games=games, genre_videos=genre_videos)


@app.route('/strategy-games')
def strategy_games():
    games = fetch_games('strategy_games')
    genre_videos = [
        '5KdE0p2joJw',
        'J8SBp4SyvLc',
        'fXxe897bW-A'
    ]
    return render_template('genre_games.html', genre='Strategy', games=games, genre_videos=genre_videos)


@app.route('/mobile_games')
def mobile_games():
    games = fetch_mobile_games()  # Fetch games from the mobilegame table in RDS
    genre_videos = [
        '44MOkHyEvJs', 'R8htow_6tRc', 'QLuShrJyurE', 'mfm0VHQJZxE',
        'GajGrj7HLQM', 'uA16fjZArkY', 'w8vPZrMFiZ4', 'zCX-Tz8KpXE',
        'Nkhvl4Sazj4', 'ot7uXNQskhs', 'M0niPfYZaaI',
    ]
    return render_template('mobileGames.html', genre='Mobile', games=games, genre_videos=genre_videos)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the new schema with the additional fields
    app.run(debug=True)


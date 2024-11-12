from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from utils import fetch_cached_games, fetch_game_details, fetch_google_play_games, load_game_data
import bcrypt, pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning

db = SQLAlchemy(app)

# Setting up RDS connection
def connect_to_db():
    return pymysql.connect(
        host='gamesite.cg1ttynegix3.us-west-2.rds.amazonaws.com',
        user='admin',
        password='VpR6koaUyDcvLK67lcV9',
        database='site_schema',
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
    # Fetch Steam games from Steam API
    steam_games = fetch_game_details([1938090, 1880360, 1240440, 2406770])  # Example AppIDs

    # Fetch Google Play Store placeholders
    google_play_games = fetch_google_play_games()

    return render_template('home.html', google_play_games=google_play_games, steam_games=steam_games)

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


# Mock dataset for demonstration purposes
mock_games = [
    {'name': 'Call of Duty: Modern Warfare', 'description': 'First-person shooter game',
     'image_url': 'https://via.placeholder.com/150', 'link': '#'},
    {'name': 'Monster Hunter Rise', 'description': 'Action RPG game with monster battles',
     'image_url': 'https://via.placeholder.com/150', 'link': '#'},
    {'name': 'Halo Infinite', 'description': 'Sci-fi FPS adventure', 'image_url': 'https://via.placeholder.com/150',
     'link': '#'},
]


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    # Filter the mock dataset to find matches
    results = [game for game in mock_games if query in game['name'].lower()]

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
    games = fetch_games('action_games')  # Fetch from the corresponding table
    return render_template('genre_games.html', genre='Action', games=games)

@app.route('/adventure-games')
def adventure_games():
    games = fetch_games('adventure_games')
    return render_template('genre_games.html', genre='Adventure', games=games)

# Route for Early Access Games
@app.route('/earlyaccess-games')
def earlyaccess_games():
    games = fetch_games('earlyaccess_games')
    return render_template('genre_games.html', genre='Early Access', games=games)

# Route for Free Games
@app.route('/free-games')
def free_games():
    games = fetch_games('free_games')
    return render_template('genre_games.html', genre='Free to Play', games=games)

# Add additional routes for each genre as needed
@app.route('/indie-games')
def indie_games():
    games = fetch_games('indie_games')
    return render_template('genre_games.html', genre='Indie', games=games)

@app.route('/mmo-games')
def mmo_games():
    games = fetch_games('mmo_games')
    return render_template('genre_games.html', genre='MMO', games=games)

@app.route('/rpg-games')
def rpg_games():
    games = fetch_games('rpg_games')
    return render_template('genre_games.html', genre='RPG', games=games)

@app.route('/simulation-games')
def simulation_games():
    games = fetch_games('simulation_games')
    return render_template('genre_games.html', genre='Simulation', games=games)

@app.route('/sports-games')
def sports_games():
    games = fetch_games('sports_games')
    return render_template('genre_games.html', genre='Sports', games=games)

@app.route('/strategy-games')
def strategy_games():
    games = fetch_games('strategy_games')
    return render_template('genre_games.html', genre='Strategy', games=games)


@app.route('/mobile_games')
def mobile_games():
    games = fetch_mobile_games()  # Fetch games from the mobilegame table in RDS
    return render_template('mobileGames.html', games=games)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the new schema with the additional fields
    app.run(debug=True)


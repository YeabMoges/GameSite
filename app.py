from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from utils import fetch_cached_games, fetch_game_details, fetch_google_play_games, load_game_data
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning

db = SQLAlchemy(app)


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
    return render_template('actionGames.html')


@app.route('/mobile_games')
def mobile_games():
    games = load_game_data()  # Ensure this loads the JSON data
    print(f"Games loaded: {games}")  # Debugging
    return render_template('mobileGames.html', games=games)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the new schema with the additional fields
    app.run(debug=True)


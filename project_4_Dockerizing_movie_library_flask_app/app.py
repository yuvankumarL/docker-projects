from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
import requests
from flask import flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database connection
def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

# User model
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        user_obj = User()
        user_obj.id = user['id']
        user_obj.username = user['username']
        return user_obj
    return None


@app.route('/')
@login_required
def home():
    db = get_db()
    lists = db.execute('SELECT * FROM lists WHERE user_id = ?', (current_user.id,)).fetchall()
    return render_template('home.html', lists=lists)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        if user:
            user_obj = User()
            user_obj.id = user['id']
            user_obj.username = user['username']
            login_user(user_obj)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form['query']
        url = f'http://www.omdbapi.com/?i=tt3896198&apikey=f339223a&s={query}'
        response = requests.get(url)
        data = response.json()
        if data['Response'] == 'True':
            movies = data['Search']
            db = get_db()
            lists = db.execute('SELECT * FROM lists WHERE user_id = ?', (current_user.id,)).fetchall()
            return render_template('search.html', movies=movies, lists=lists)
        else:
            flash('No movies found')
    return render_template('search.html')

@app.route('/lists')
@login_required
def lists():
    db = get_db()
    lists = db.execute('SELECT * FROM lists WHERE user_id = ?', (current_user.id,)).fetchall()
    return render_template('lists.html', lists=lists)

@app.route('/create_list', methods=['POST'])
@login_required
def create_list():
    name = request.form.get('name')
    is_public = request.form.get('is_public') == 'on'  # Default to '0' if not checked
    print(f"Raw is_public value from form: {is_public}")  # Debug print

    # Explicitly convert the value to 0 or 1
    is_public = 1 if request.form.get('is_public') == 'on' else 0
    print(f"Converted is_public value: {is_public}")  # Debug print

    db = get_db()
    try:
        db.execute('INSERT INTO lists (name, user_id, is_public) VALUES (?, ?, ?)', (name, current_user.id, is_public))
        db.commit()
        print(f"List created: name={name}, user_id={current_user.id}, is_public={is_public}")  # Debug print
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")
        flash('An error occurred while creating the list.')
        return redirect(url_for('lists'))
    
    return redirect(url_for('lists'))


@app.route('/list/<int:list_id>')
@login_required
def list_details(list_id):
    db = get_db()
    list_data = db.execute('SELECT * FROM lists WHERE id = ?', (list_id,)).fetchone()
    if list_data:
        if list_data['user_id'] != current_user.id and not list_data['is_public']:
            flash('Access denied')
            print('Access denied')
            return redirect(url_for('lists'))
        
        # Fetch the movie titles, years, and poster URLs for this list
        movies = db.execute('''
            SELECT m.title, m.year, m.poster FROM movies m
            JOIN list_movies lm ON m.id = lm.movie_id
            WHERE lm.list_id = ?
        ''', (list_id,)).fetchall()

        return render_template('list_details.html', list=list_data, movies=movies)
    else:
        flash('List not found')
        print('List not found')
        return redirect(url_for('lists'))
        

def fetch_movie_data(movie_id):
    # Simulate fetching movie data from a database or API based on the movie ID
    # In a real application, this function would interact with your data source (e.g., database, API)
    # and return the movie data in a suitable format (e.g., dictionary)
    movie_data = {
        'id': movie_id,
        'title': f'Movie Title {movie_id}',
        'year': 2022,  # Assuming a specific year for demonstration
        'poster': f'https://example.com/posters/{movie_id}.jpg'  # Example URL for movie poster
    }
    return movie_data

@app.route('/add_to_list', methods=['POST'])
@login_required
def add_to_list():
    list_id = request.form.get('list_id')
    movie_title = request.form.get('movie_title')
    movie_year = request.form.get('movie_year')
    movie_poster = request.form.get('movie_poster')

    if not list_id or not movie_title:
        flash('Error: List ID or Movie Title missing.')
        return redirect(url_for('search'))

    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if the movie already exists in the 'movies' table
        cursor.execute('SELECT id FROM movies WHERE title = ? AND year = ?',
                       (movie_title, movie_year))
        existing_movie = cursor.fetchone()

        if existing_movie:
            movie_id = existing_movie['id']
        else:
            # Insert the movie into the 'movies' table
            cursor.execute('INSERT INTO movies (title, year, poster) VALUES (?, ?, ?)',
                           (movie_title, movie_year, movie_poster))
            movie_id = cursor.lastrowid

        # Insert the movie ID and list ID into the 'list_movies' table
        cursor.execute('INSERT INTO list_movies (list_id, movie_id) VALUES (?, ?)', (list_id, movie_id))

        db.commit()
        flash('Movie added to list successfully!')
        print('Movie added to list successfully!')

    except sqlite3.IntegrityError as e:
        flash(f'Error adding movie to list: {e}')
        print(f'Error adding movie to list: {e}')
    except Exception as e:
        flash(f'Error: {e}')
        print(f'Error: {e}')

    return redirect(url_for('list_details', list_id=list_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

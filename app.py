from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


# -----------------------------
# STRONA GŁÓWNA – LISTA FILMÓW
# -----------------------------
@app.route("/")
def home():
    db = sqlite3.connect('movies.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    db.close()
    return render_template('index.html', movies=movies)


# -----------------------------
# DODAWANIE FILMU
# -----------------------------
@app.route("/addMovie", methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movieTitle = request.form.get('title')
        movieYear = request.form.get('year')
        movieActors = request.form.get('actors')

        # WALIDACJA
        if not movieTitle:
            return render_template('add.html', error="Movie title can not be empty")

        if not movieYear:
            return render_template('add.html', error="Movie year can not be empty")

        if not movieActors:
            return render_template('add.html', error="Movie actors can not be empty")

        # ZAPIS DO BAZY
        db = sqlite3.connect('movies.db')
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
            (movieTitle, movieYear, movieActors)
        )
        db.commit()
        db.close()

        return redirect(url_for('home'))

    return render_template('add.html')


# -----------------------------
# USUWANIE FILMÓW
# -----------------------------
@app.route("/delete", methods=["POST"])
def delete_movies():
    movies_to_remove_ids = request.form.getlist('movieToRemove')

    if movies_to_remove_ids:
        db = sqlite3.connect('movies.db')
        cursor = db.cursor()
        cursor.executemany("DELETE FROM movies WHERE id = ?", [(i,) for i in movies_to_remove_ids])
        db.commit()
        db.close()

    return redirect(url_for('home'))


# -----------------------------
# URUCHOMIENIE APLIKACJI
# -----------------------------
if __name__ == "__main__":
    app.run()

